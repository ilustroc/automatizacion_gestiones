import logging
import os
from dataclasses import dataclass
from pathlib import Path
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from dotenv import load_dotenv

from app.exceptions import ConfiguracionError


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_OUTPUT_DIR = BASE_DIR / "data" / "output"
LOGS_DIR = BASE_DIR / "logs"
LOG_FILE = LOGS_DIR / "proceso.log"


@dataclass(frozen=True, slots=True)
class DatabaseConfig:
    engine: str
    host: str
    port: int
    name: str
    user: str
    password: str
    connect_timeout: int = 15
    read_timeout: int = 120
    write_timeout: int = 120
    charset: str = "utf8mb4"


@dataclass(frozen=True, slots=True)
class SourceDatabaseConfig(DatabaseConfig):
    """Configuracion de la base ESCALL, usada solo para lectura."""


@dataclass(frozen=True, slots=True)
class TargetDatabaseConfig(DatabaseConfig):
    """Configuracion de la base local que recibe los datos procesados."""


@dataclass(frozen=True, slots=True)
class SmtpConfig:
    host: str
    port: int
    use_ssl: bool
    user: str
    password: str
    from_email: str
    from_name: str


@dataclass(frozen=True, slots=True)
class MailConfig:
    gerencia: str
    supervisor: str
    empresa_impulse: str


@dataclass(frozen=True, slots=True)
class AppConfig:
    batch_size: int
    exportar_excel: bool
    enviar_correos: bool
    timezone: str


def cargar_configuracion(
    ruta_env: Path | str | None = None,
    *,
    override: bool = False,
) -> None:
    """Carga .env sin exponer ni transformar las credenciales."""
    load_dotenv(Path(ruta_env) if ruta_env else BASE_DIR / ".env", override=override)
    DATA_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    LOGS_DIR.mkdir(parents=True, exist_ok=True)


def obtener_configuracion_source_db() -> SourceDatabaseConfig:
    return _obtener_configuracion_db(
        SourceDatabaseConfig,
        prefijo="SOURCE_DB",
        nombre_defecto="escarperu_software",
        etiqueta="origen ESCALL",
    )


def obtener_configuracion_target_db() -> TargetDatabaseConfig:
    return _obtener_configuracion_db(
        TargetDatabaseConfig,
        prefijo="TARGET_DB",
        nombre_defecto="automatizacion_gestiones",
        etiqueta="destino local",
    )


def obtener_configuracion_smtp() -> SmtpConfig:
    variables = {
        "SMTP_HOST": os.getenv("SMTP_HOST", "").strip(),
        "SMTP_PORT": os.getenv("SMTP_PORT", "465").strip(),
        "SMTP_USER": os.getenv("SMTP_USER", "").strip(),
        "SMTP_PASSWORD": os.getenv("SMTP_PASSWORD", ""),
        "SMTP_FROM": os.getenv("SMTP_FROM", "").strip(),
        "SMTP_FROM_NAME": os.getenv(
            "SMTP_FROM_NAME", "Automatizacion de Gestiones"
        ).strip(),
    }
    _validar_requeridos(variables, "SMTP")
    _validar_correo(variables["SMTP_USER"], "SMTP_USER")
    _validar_correo(variables["SMTP_FROM"], "SMTP_FROM")

    return SmtpConfig(
        host=variables["SMTP_HOST"],
        port=_entero_positivo(variables["SMTP_PORT"], "SMTP_PORT"),
        use_ssl=_booleano(os.getenv("SMTP_USE_SSL", "true"), "SMTP_USE_SSL"),
        user=variables["SMTP_USER"],
        password=variables["SMTP_PASSWORD"],
        from_email=variables["SMTP_FROM"],
        from_name=variables["SMTP_FROM_NAME"],
    )


def obtener_configuracion_correos(
    requeridos: set[str] | None = None,
) -> MailConfig:
    variables = {
        "MAIL_GERENCIA": os.getenv("MAIL_GERENCIA", "").strip(),
        "MAIL_SUPERVISOR": os.getenv("MAIL_SUPERVISOR", "").strip(),
        "MAIL_EMPRESA_IMPULSE": os.getenv("MAIL_EMPRESA_IMPULSE", "").strip(),
    }
    nombres_requeridos = requeridos or set(variables)
    seleccion = {
        nombre: valor
        for nombre, valor in variables.items()
        if nombre in nombres_requeridos
    }
    _validar_requeridos(seleccion, "destinatarios de reportes")
    for nombre, correo in seleccion.items():
        _validar_correo(correo, nombre)
    return MailConfig(
        gerencia=variables["MAIL_GERENCIA"],
        supervisor=variables["MAIL_SUPERVISOR"],
        empresa_impulse=variables["MAIL_EMPRESA_IMPULSE"],
    )


def obtener_configuracion_app() -> AppConfig:
    batch_size = _entero_positivo(os.getenv("BATCH_SIZE", "1000"), "BATCH_SIZE")
    timezone = os.getenv("APP_TIMEZONE", "America/Lima").strip()
    try:
        ZoneInfo(timezone)
    except ZoneInfoNotFoundError as error:
        raise ConfiguracionError(f"APP_TIMEZONE no es valida: {timezone}") from error

    return AppConfig(
        batch_size=batch_size,
        exportar_excel=_booleano(os.getenv("EXPORTAR_EXCEL", "true"), "EXPORTAR_EXCEL"),
        enviar_correos=_booleano(os.getenv("ENVIAR_CORREOS", "false"), "ENVIAR_CORREOS"),
        timezone=timezone,
    )


def configurar_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(LOG_FILE, encoding="utf-8"),
            logging.StreamHandler(),
        ],
        force=True,
    )


def _obtener_configuracion_db(
    clase: type[SourceDatabaseConfig] | type[TargetDatabaseConfig],
    *,
    prefijo: str,
    nombre_defecto: str,
    etiqueta: str,
) -> SourceDatabaseConfig | TargetDatabaseConfig:
    variables = {
        f"{prefijo}_ENGINE": os.getenv(f"{prefijo}_ENGINE", "mysql").strip(),
        f"{prefijo}_HOST": os.getenv(f"{prefijo}_HOST", "").strip(),
        f"{prefijo}_PORT": os.getenv(f"{prefijo}_PORT", "3306").strip(),
        f"{prefijo}_NAME": os.getenv(f"{prefijo}_NAME", nombre_defecto).strip(),
        f"{prefijo}_USER": os.getenv(f"{prefijo}_USER", "").strip(),
        f"{prefijo}_PASSWORD": os.getenv(f"{prefijo}_PASSWORD", ""),
        f"{prefijo}_CONNECT_TIMEOUT": os.getenv(
            f"{prefijo}_CONNECT_TIMEOUT", "15"
        ).strip(),
        f"{prefijo}_READ_TIMEOUT": os.getenv(
            f"{prefijo}_READ_TIMEOUT", "120"
        ).strip(),
        f"{prefijo}_WRITE_TIMEOUT": os.getenv(
            f"{prefijo}_WRITE_TIMEOUT", "120"
        ).strip(),
    }
    _validar_requeridos(variables, f"base de datos {etiqueta}")

    engine = variables[f"{prefijo}_ENGINE"].lower()
    if engine not in {"mysql", "mariadb"}:
        raise ConfiguracionError(
            f"{prefijo}_ENGINE debe ser mysql o mariadb."
        )

    return clase(
        engine=engine,
        host=variables[f"{prefijo}_HOST"],
        port=_entero_positivo(variables[f"{prefijo}_PORT"], f"{prefijo}_PORT"),
        name=variables[f"{prefijo}_NAME"],
        user=variables[f"{prefijo}_USER"],
        password=variables[f"{prefijo}_PASSWORD"],
        connect_timeout=_entero_positivo(
            variables[f"{prefijo}_CONNECT_TIMEOUT"],
            f"{prefijo}_CONNECT_TIMEOUT",
        ),
        read_timeout=_entero_positivo(
            variables[f"{prefijo}_READ_TIMEOUT"],
            f"{prefijo}_READ_TIMEOUT",
        ),
        write_timeout=_entero_positivo(
            variables[f"{prefijo}_WRITE_TIMEOUT"],
            f"{prefijo}_WRITE_TIMEOUT",
        ),
    )


def _validar_requeridos(variables: dict[str, str], etiqueta: str) -> None:
    faltantes = [nombre for nombre, valor in variables.items() if valor == ""]
    if faltantes:
        raise ConfiguracionError(
            f"Faltan variables para {etiqueta}: " + ", ".join(faltantes)
        )


def _entero_positivo(valor: str, nombre: str) -> int:
    try:
        numero = int(valor)
    except (TypeError, ValueError) as error:
        raise ConfiguracionError(f"{nombre} debe ser un numero entero.") from error
    if numero <= 0:
        raise ConfiguracionError(f"{nombre} debe ser mayor que cero.")
    return numero


def _booleano(valor: str, nombre: str) -> bool:
    normalizado = str(valor).strip().lower()
    if normalizado in {"true", "1", "si", "yes"}:
        return True
    if normalizado in {"false", "0", "no"}:
        return False
    raise ConfiguracionError(f"{nombre} debe ser true o false.")


def _validar_correo(correo: str, nombre: str) -> None:
    if "@" not in correo or correo.startswith("@") or correo.endswith("@"):
        raise ConfiguracionError(f"{nombre} debe contener un correo valido.")


# Alias temporal para modulos academicos de la version anterior.
def obtener_configuracion_db() -> TargetDatabaseConfig:
    return obtener_configuracion_target_db()
