import logging
import os
from datetime import date

from psycopg2 import Error as PostgreSQLError

from app.config import (
    ConfiguracionError,
    cargar_configuracion,
    configurar_logging,
    obtener_configuracion_db,
)
from app.repositories.carga_gestion_repository import CargaGestionRepository
from app.repositories.database import Database
from app.repositories.envio_reporte_repository import EnvioReporteRepository
from app.repositories.gestion_repository import GestionRepository
from app.repositories.log_proceso_repository import LogProcesoRepository
from app.repositories.reporte_repository import ReporteRepository
from app.services.descargador_service import DescargadorService
from app.services.homologador_service import HomologadorService
from app.services.limpiador_service import LimpiadorService
from app.services.notificacion_service import NotificacionService
from app.services.reporte_service import ReporteService
from app.services.validador_service import ValidadorService


def main() -> None:
    cargar_configuracion()
    configurar_logging()

    try:
        db_config = obtener_configuracion_db()
    except ConfiguracionError as error:
        logging.error(str(error))
        print(str(error))
        print("Configura el archivo .env con las credenciales de Supabase/PostgreSQL.")
        return

    db = Database(db_config)
    id_carga = None

    try:
        db.conectar()
        logging.info("Conexion a PostgreSQL/Supabase establecida")

        gestion_repository = GestionRepository(db)
        carga_repository = CargaGestionRepository(db)
        log_repository = LogProcesoRepository(db)
        reporte_repository = ReporteRepository(db)
        envio_repository = EnvioReporteRepository(db)

        descargador = DescargadorService(gestion_repository)
        limpiador = LimpiadorService()
        homologador = HomologadorService()
        validador = ValidadorService()
        reporte_service = ReporteService(reporte_repository)
        NotificacionService(envio_repository)

        hoy = date.today()
        consulta_origen = os.getenv("DATABASE_SOURCE_QUERY")
        id_carga = carga_repository.crear_carga(
            periodo_desde=hoy,
            periodo_hasta=hoy,
            origen="BASE_DATOS",
            nombre_sp=os.getenv("DATABASE_SOURCE_SP"),
        )
        log_repository.registrar("Inicio del proceso de gestiones", id_carga=id_carga)

        df_origen = descargador.obtener_desde_base_datos(consulta_origen)
        total_descargados = len(df_origen)
        logging.info("Registros obtenidos desde base de datos: %s", total_descargados)

        if df_origen.empty:
            carga_repository.finalizar_carga(
                id_carga=id_carga,
                registros_descargados=0,
                registros_insertados=0,
                registros_duplicados=0,
                estado="FINALIZADO",
                observacion="No se encontraron gestiones para procesar.",
            )
            log_repository.registrar(
                "No se encontraron gestiones para procesar.",
                id_carga=id_carga,
            )
            db.confirmar()
            print("No se encontraron gestiones para procesar.")
            return

        validador.validar_columnas(df_origen)
        df_limpio = limpiador.limpiar_dataframe(df_origen)
        df_homologado = homologador.homologar_dataframe(df_limpio)
        df_validos, descartados = validador.obtener_registros_validos(df_homologado)
        df_sin_duplicados, duplicados_en_lote = validador.eliminar_duplicados(df_validos)
        df_final = validador.agregar_clave_unica(df_sin_duplicados)

        gestiones = df_final.to_dict(orient="records")
        insertados, duplicados_bd = gestion_repository.insertar_gestiones(
            gestiones=gestiones,
            id_carga=id_carga,
        )
        total_duplicados = duplicados_en_lote + duplicados_bd

        carga_repository.finalizar_carga(
            id_carga=id_carga,
            registros_descargados=total_descargados,
            registros_insertados=insertados,
            registros_duplicados=total_duplicados,
            estado="FINALIZADO",
            observacion=f"Registros descartados por validacion: {descartados}",
        )
        log_repository.registrar(
            (
                "Proceso finalizado. "
                f"Descargados: {total_descargados}, insertados: {insertados}, "
                f"duplicados: {total_duplicados}, descartados: {descartados}"
            ),
            id_carga=id_carga,
        )

        resumen = reporte_service.obtener_resumen_desde_bd()
        db.confirmar()

        print("Proceso finalizado correctamente")
        print(f"- Registros descargados: {total_descargados}")
        print(f"- Registros insertados: {insertados}")
        print(f"- Registros duplicados: {total_duplicados}")
        print(f"- Registros descartados por validacion: {descartados}")
        print(reporte_service.formatear_resumen_bd(resumen))

    except (PostgreSQLError, ValueError) as error:
        logging.exception("Error durante el proceso")
        db.revertir()
        if id_carga is not None:
            try:
                carga_repository.finalizar_carga(
                    id_carga=id_carga,
                    registros_descargados=0,
                    registros_insertados=0,
                    registros_duplicados=0,
                    estado="ERROR",
                    observacion=str(error),
                )
                log_repository.registrar(str(error), nivel="ERROR", id_carga=id_carga)
                db.confirmar()
            except PostgreSQLError:
                db.revertir()
        print(f"Error durante el proceso: {error}")
    finally:
        db.cerrar()


if __name__ == "__main__":
    main()

