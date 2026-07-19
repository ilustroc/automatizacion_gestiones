import argparse
import logging
from datetime import date, datetime, time, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

from app.config import (
    DATA_OUTPUT_DIR,
    cargar_configuracion,
    configurar_logging,
    obtener_configuracion_app,
    obtener_configuracion_correos,
    obtener_configuracion_smtp,
    obtener_configuracion_source_db,
    obtener_configuracion_target_db,
)
from app.exceptions import AutomatizacionError, ConfiguracionError
from app.repositories.control_descarga_repository import ControlDescargaRepository
from app.repositories.carga_gestion_repository import CargaGestionRepository
from app.repositories.database import DatabaseConnection
from app.repositories.envio_reporte_repository import EnvioReporteRepository
from app.repositories.gestion_procesada_repository import GestionProcesadaRepository
from app.repositories.log_proceso_repository import LogProcesoRepository
from app.repositories.reporte_repository import ReporteRepository
from app.repositories.source_gestion_repository import SourceGestionRepository
from app.services.descargador_service import DescargadorService
from app.services.diagnostico_service import DiagnosticoService
from app.services.homologador_service import HomologadorService
from app.services.limpiador_service import LimpiadorService
from app.services.notificacion_service import NotificacionService
from app.services.procesador_gestiones_service import ProcesadorGestionesService
from app.services.reporte_gerencia_service import ReporteGerenciaService
from app.services.reporte_impulse_service import ReporteImpulseService
from app.services.reporte_promesas_service import ReportePromesasService
from app.services.validador_service import ValidadorService


def construir_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Descarga gestiones de ESCALL, las procesa y las almacena en MySQL local."
        )
    )
    parser.add_argument(
        "--modo",
        choices=["diagnostico", "manual", "pendiente", "automatico", "reporte", "interfaz"],
        default="pendiente",
    )
    parser.add_argument("--interfaz", action="store_true")
    parser.add_argument(
        "--reporte", choices=["promesas", "impulse", "gerencia", "todos"]
    )
    parser.add_argument("--fecha-inicio", help="Fecha inicial inclusiva YYYY-MM-DD.")
    parser.add_argument("--fecha-fin", help="Fecha final inclusiva YYYY-MM-DD.")
    parser.add_argument("--fecha-desde", help="Inicio YYYY-MM-DD HH:MM:SS.")
    parser.add_argument("--fecha-hasta", help="Fin exclusivo YYYY-MM-DD HH:MM:SS.")
    parser.add_argument("--descripcion", default="Solicitud registrada por consola.")
    grupo_envio = parser.add_mutually_exclusive_group()
    grupo_envio.add_argument(
        "--solo-generar", action="store_true", help="Genera archivos sin enviar correo."
    )
    grupo_envio.add_argument(
        "--enviar", action="store_true", help="Confirma el envio real por SMTP."
    )
    parser.add_argument("--sin-correos", action="store_true", help=argparse.SUPPRESS)
    return parser


def main(argv: list[str] | None = None) -> int:
    cargar_configuracion()
    configurar_logging()
    args = construir_parser().parse_args(argv)

    try:
        if args.interfaz or args.modo == "interfaz":
            return ejecutar_interfaz()
        if args.reporte or args.modo == "reporte":
            if not args.reporte:
                raise ValueError("El modo reporte requiere --reporte.")
            return ejecutar_reportes(args)
        if args.modo == "diagnostico":
            return ejecutar_diagnostico()
        return ejecutar_procesamiento(args)
    except (AutomatizacionError, ValueError) as error:
        logging.error("%s", error)
        print(f"ERROR: {error}")
        return 1
    except Exception as error:
        logging.exception("Error no controlado durante la ejecucion.")
        print(f"ERROR: {error}")
        return 1


def ejecutar_diagnostico() -> int:
    print("Diagnostico de conexiones y estructura")
    source_db: DatabaseConnection | None = None
    target_db: DatabaseConnection | None = None
    errores = 0

    try:
        source_db = DatabaseConnection(obtener_configuracion_source_db()).conectar()
        print("[OK] Conexion origen ESCALL")
    except (AutomatizacionError, ConfiguracionError) as error:
        errores += 1
        print(f"[ERROR] Origen ESCALL: {error}")

    try:
        target_db = DatabaseConnection(obtener_configuracion_target_db()).conectar()
        print("[OK] Conexion destino local")
    except (AutomatizacionError, ConfiguracionError) as error:
        errores += 1
        print(f"[ERROR] Destino local: {error}")

    try:
        if source_db is not None:
            servicio = DiagnosticoService(source_db=source_db)
            try:
                origen = servicio.diagnosticar_origen()
                print(f"[OK] Version origen: {origen['version']}")
                print("[OK] Tabla gestiones y Stored Procedure verificados")
                print("Columnas origen: " + ", ".join(origen["columnas"]))
            except AutomatizacionError as error:
                errores += 1
                print(f"[ERROR] Estructura origen: {error}")
        if target_db is not None:
            servicio = DiagnosticoService(target_db=target_db)
            try:
                destino = servicio.diagnosticar_destino()
                print(f"[OK] Version destino: {destino['version']}")
                print("Tablas destino: " + ", ".join(destino["tablas"]))
            except AutomatizacionError as error:
                errores += 1
                print(f"[ERROR] Estructura destino: {error}")
    finally:
        if source_db is not None:
            source_db.cerrar()
        if target_db is not None:
            target_db.cerrar()

    if errores:
        print("Diagnostico finalizado con observaciones. No se modificaron datos.")
        return 1
    print("Diagnostico finalizado correctamente. No se modificaron datos.")
    return 0


def ejecutar_procesamiento(args: argparse.Namespace) -> int:
    app_config = obtener_configuracion_app()
    target_db = DatabaseConnection(obtener_configuracion_target_db())
    source_db: DatabaseConnection | None = None
    control: dict | None = None
    control_repository: ControlDescargaRepository | None = None
    log_repository: LogProcesoRepository | None = None
    procesamiento_iniciado = False

    try:
        target_db.conectar()
        control_repository = ControlDescargaRepository(target_db)
        log_repository = LogProcesoRepository(target_db)
        control = obtener_control_descarga(args, control_repository, app_config.timezone)
        target_db.commit()
        if control is None:
            print("No hay descargas pendientes para procesar.")
            return 0

        source_db = DatabaseConnection(obtener_configuracion_source_db()).conectar()
        source_repository = SourceGestionRepository(source_db)
        procesador = ProcesadorGestionesService(
            target_db=target_db,
            control_repository=control_repository,
            gestion_repository=GestionProcesadaRepository(
                target_db, batch_size=app_config.batch_size
            ),
            log_repository=log_repository,
            descargador=DescargadorService(source_repository),
            limpiador=LimpiadorService(),
            homologador=HomologadorService(),
            validador=ValidadorService(),
            carga_repository=CargaGestionRepository(target_db),
        )
        procesamiento_iniciado = True
        resultado = procesador.procesar_control(control)
        _mostrar_resultado(resultado.como_dict())
        return 0
    except Exception as error:
        if (
            not procesamiento_iniciado
            and control
            and control_repository
            and log_repository
        ):
            _marcar_error_externo(
                target_db,
                control_repository,
                log_repository,
                int(control["id_control"]),
                error,
            )
        raise
    finally:
        if source_db is not None:
            source_db.cerrar()
        target_db.cerrar()


def obtener_control_descarga(
    args: argparse.Namespace,
    repository: ControlDescargaRepository,
    timezone: str,
) -> dict | None:
    if args.modo == "pendiente":
        return repository.obtener_pendiente()

    if args.modo == "manual":
        fecha_desde, fecha_hasta = resolver_rango(args)
        id_control = repository.crear_control(
            fecha_desde,
            fecha_hasta,
            "MANUAL",
            args.descripcion,
        )
        return repository.obtener_por_id(id_control)

    if args.modo == "automatico":
        if args.fecha_desde or args.fecha_hasta:
            fecha_desde, fecha_hasta = resolver_rango(args)
        else:
            ahora = datetime.now(ZoneInfo(timezone)).replace(tzinfo=None)
            fecha_desde, fecha_hasta = repository.calcular_ultima_hora(ahora)
        id_control = repository.crear_control(
            fecha_desde,
            fecha_hasta,
            "AUTOMATICA",
            "Descarga automatica de la ultima hora cerrada.",
        )
        return repository.obtener_por_id(id_control)

    raise ValueError(f"El modo {args.modo} no ejecuta descargas.")


def resolver_rango(args: argparse.Namespace) -> tuple[datetime, datetime]:
    if args.fecha_desde or args.fecha_hasta:
        if not args.fecha_desde or not args.fecha_hasta:
            raise ValueError("Debe indicar --fecha-desde y --fecha-hasta juntos.")
        desde = datetime.strptime(args.fecha_desde, "%Y-%m-%d %H:%M:%S")
        hasta = datetime.strptime(args.fecha_hasta, "%Y-%m-%d %H:%M:%S")
    else:
        if not args.fecha_inicio or not args.fecha_fin:
            raise ValueError(
                "Debe indicar --fecha-inicio y --fecha-fin, o un rango con hora."
            )
        fecha_inicio = datetime.strptime(args.fecha_inicio, "%Y-%m-%d").date()
        fecha_fin = datetime.strptime(args.fecha_fin, "%Y-%m-%d").date()
        desde = datetime.combine(fecha_inicio, time.min)
        hasta = datetime.combine(fecha_fin + timedelta(days=1), time.min)
    if hasta <= desde:
        raise ValueError("La fecha final debe ser mayor que la fecha inicial.")
    return desde, hasta


def ejecutar_reportes(args: argparse.Namespace) -> int:
    target_db = DatabaseConnection(obtener_configuracion_target_db()).conectar()
    try:
        app_config = obtener_configuracion_app()
        repository = ReporteRepository(target_db)
        envio_repository = EnvioReporteRepository(target_db)
        tipos = (
            ["promesas", "impulse", "gerencia"]
            if args.reporte == "todos"
            else [args.reporte]
        )
        desde, hasta = _rango_reporte(args, app_config.timezone)
        enviar = bool(args.enviar and not args.sin_correos)
        if enviar and not app_config.enviar_correos:
            raise ConfiguracionError(
                "Para enviar correos reales configure ENVIAR_CORREOS=\"true\" "
                "y use --enviar."
            )
        notificador = None
        correos = None
        if enviar:
            variables_correo = {
                "promesas": "MAIL_SUPERVISOR",
                "impulse": "MAIL_EMPRESA_IMPULSE",
                "gerencia": "MAIL_GERENCIA",
            }
            correos = obtener_configuracion_correos(
                {variables_correo[tipo] for tipo in tipos}
            )
            notificador = NotificacionService(
                envio_repository,
                obtener_configuracion_smtp(),
            )

        exitos = True
        for tipo in tipos:
            servicio, datos, destinatario = _preparar_reporte(
                tipo, repository, correos, desde, hasta
            )
            periodo = f"{desde:%Y-%m-%d %H:%M:%S} a {hasta:%Y-%m-%d %H:%M:%S}"
            html = (
                servicio.generar_html(datos, periodo)
                if tipo == "impulse"
                else servicio.generar_html(datos)
            )
            adjunto = None
            if app_config.exportar_excel or args.solo_generar:
                adjunto = DATA_OUTPUT_DIR / (
                    f"reporte_{tipo}_{datetime.now():%Y%m%d_%H%M%S}.xlsx"
                )
                servicio.exportar_excel(datos, adjunto)
                print(f"[OK] Excel generado: {adjunto}")
            repository.registrar_reporte(
                servicio.tipo_reporte,
                desde,
                hasta,
                adjunto,
            )
            asunto = servicio.crear_asunto(date.today())
            if enviar and notificador is not None:
                enviado = notificador.enviar_html(
                    servicio.tipo_reporte,
                    destinatario,
                    asunto,
                    html,
                    adjunto,
                )
                exitos &= enviado
                print(f"[{'OK' if enviado else 'ERROR'}] Envio {tipo}: {destinatario}")
            else:
                print(f"[OK] Reporte {tipo} generado sin envio de correo.")
        target_db.commit()
        return 0 if exitos else 1
    except Exception:
        target_db.rollback()
        raise
    finally:
        target_db.cerrar()


def _preparar_reporte(tipo, repository, correos, desde, hasta):
    if tipo == "promesas":
        servicio = ReportePromesasService(repository)
        datos = servicio.obtener_datos()
        destinatario = correos.supervisor if correos else ""
    elif tipo == "impulse":
        servicio = ReporteImpulseService(repository)
        datos = servicio.obtener_datos(desde, hasta)
        destinatario = correos.empresa_impulse if correos else ""
    else:
        servicio = ReporteGerenciaService(repository)
        datos = servicio.obtener_datos(desde, hasta)
        destinatario = correos.gerencia if correos else ""
    return servicio, datos, destinatario


def _rango_reporte(args, timezone: str) -> tuple[datetime, datetime]:
    if args.fecha_desde or args.fecha_hasta or args.fecha_inicio or args.fecha_fin:
        return resolver_rango(args)
    hoy = datetime.now(ZoneInfo(timezone)).date()
    return datetime.combine(hoy, time.min), datetime.combine(
        hoy + timedelta(days=1), time.min
    )


def ejecutar_interfaz() -> int:
    from app.ui.descargas_view import DescargasView

    def probar() -> str:
        source = DatabaseConnection(obtener_configuracion_source_db())
        target = DatabaseConnection(obtener_configuracion_target_db())
        try:
            source.conectar()
            target.conectar()
            source.probar_conexion()
            target.probar_conexion()
            return "Las conexiones origen y destino responden correctamente."
        finally:
            source.cerrar()
            target.cerrar()

    def registrar(desde, hasta, tipo, descripcion) -> str:
        with DatabaseConnection(obtener_configuracion_target_db()) as target:
            id_control = ControlDescargaRepository(target).crear_control(
                desde, hasta, tipo, descripcion
            )
        return f"Descarga pendiente registrada con ID {id_control}."

    def ejecutar(desde, hasta, tipo, descripcion) -> str:
        argumentos = argparse.Namespace(
            modo="automatico" if tipo == "AUTOMATICA" else "manual",
            fecha_desde=desde.strftime("%Y-%m-%d %H:%M:%S"),
            fecha_hasta=hasta.strftime("%Y-%m-%d %H:%M:%S"),
            fecha_inicio=None,
            fecha_fin=None,
            descripcion=descripcion,
        )
        codigo = ejecutar_procesamiento(argumentos)
        if codigo != 0:
            raise RuntimeError("La descarga no pudo completarse.")
        return "Descarga ejecutada correctamente."

    def listar() -> list[dict]:
        with DatabaseConnection(obtener_configuracion_target_db()) as target:
            return ControlDescargaRepository(target).listar_ultimos()

    DescargasView(probar, registrar, ejecutar, listar).run()
    return 0


def _marcar_error_externo(db, control_repo, log_repo, id_control, error) -> None:
    try:
        db.rollback()
        control_repo.marcar_error(id_control, str(error))
        log_repo.registrar(
            "No fue posible completar la descarga.",
            nivel="ERROR",
            id_control_descarga=id_control,
            detalle_error=f"{error.__class__.__name__}: {error}",
        )
        db.commit()
    except Exception:
        db.rollback()
        logging.exception("No se pudo persistir el error externo del control.")


def _mostrar_resultado(resultado: dict) -> None:
    print("Proceso finalizado correctamente")
    print(f"- Control procesado: {resultado['id_control']}")
    print(f"- Registros origen: {resultado['leidos']}")
    print(f"- Registros insertados: {resultado['insertados']}")
    print(f"- Registros duplicados: {resultado['duplicados']}")
    print(f"- Registros invalidos: {resultado['descartados']}")


if __name__ == "__main__":
    raise SystemExit(main())
