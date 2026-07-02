import logging
import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_OUTPUT_DIR = BASE_DIR / "data" / "output"
LOGS_DIR = BASE_DIR / "logs"

OUTPUT_FILE = DATA_OUTPUT_DIR / "gestiones_limpias.xlsx"
LOG_FILE = LOGS_DIR / "proceso.log"


class ConfiguracionError(Exception):
    """Error de configuracion del proyecto."""


@dataclass
class DatabaseConfig:
    host: str
    port: int
    name: str
    user: str
    password: str
    sslmode: str = "require"


def cargar_configuracion() -> None:
    """Carga variables de entorno y asegura carpetas necesarias."""
    load_dotenv(BASE_DIR / ".env")
    DATA_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    LOGS_DIR.mkdir(parents=True, exist_ok=True)


def obtener_configuracion_db() -> DatabaseConfig:
    variables = {
        "DATABASE_HOST": os.getenv("DATABASE_HOST"),
        "DATABASE_PORT": os.getenv("DATABASE_PORT", "5432"),
        "DATABASE_NAME": os.getenv("DATABASE_NAME"),
        "DATABASE_USER": os.getenv("DATABASE_USER"),
        "DATABASE_PASSWORD": os.getenv("DATABASE_PASSWORD"),
        "DATABASE_SSLMODE": os.getenv("DATABASE_SSLMODE", "require"),
    }

    faltantes = [nombre for nombre, valor in variables.items() if not valor]
    if faltantes:
        raise ConfiguracionError(
            "Faltan variables de entorno para PostgreSQL/Supabase: "
            + ", ".join(faltantes)
        )

    return DatabaseConfig(
        host=str(variables["DATABASE_HOST"]),
        port=int(str(variables["DATABASE_PORT"])),
        name=str(variables["DATABASE_NAME"]),
        user=str(variables["DATABASE_USER"]),
        password=str(variables["DATABASE_PASSWORD"]),
        sslmode=str(variables["DATABASE_SSLMODE"]),
    )


def configurar_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(LOG_FILE, encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )
