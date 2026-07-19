import logging
import traceback

import pandas as pd

from app.models.resultado_proceso import ResultadoProceso
from app.repositories.carga_gestion_repository import CargaGestionRepository
from app.repositories.control_descarga_repository import ControlDescargaRepository
from app.repositories.database import DatabaseConnection
from app.repositories.gestion_procesada_repository import GestionProcesadaRepository
from app.repositories.log_proceso_repository import LogProcesoRepository
from app.services.descargador_service import DescargadorService
from app.services.homologador_service import HomologadorService
from app.services.limpiador_service import LimpiadorService
from app.services.validador_service import ValidadorService


class ProcesadorGestionesService:
    def __init__(
        self,
        target_db: DatabaseConnection,
        control_repository: ControlDescargaRepository,
        gestion_repository: GestionProcesadaRepository,
        log_repository: LogProcesoRepository,
        descargador: DescargadorService,
        limpiador: LimpiadorService,
        homologador: HomologadorService,
        validador: ValidadorService,
        carga_repository: CargaGestionRepository | None = None,
    ):
        self.target_db = target_db
        self.control_repository = control_repository
        self.gestion_repository = gestion_repository
        self.log_repository = log_repository
        self.descargador = descargador
        self.limpiador = limpiador
        self.homologador = homologador
        self.validador = validador
        self.carga_repository = carga_repository

    def procesar_control(self, control: dict) -> ResultadoProceso:
        id_control = int(control["id_control"])
        id_carga: int | None = None
        try:
            self.control_repository.marcar_en_proceso(id_control)
            if self.carga_repository is not None:
                id_carga = self.carga_repository.crear_carga(id_control)
            self.log_repository.registrar(
                "Inicio de descarga desde ESCALL.",
                id_control_descarga=id_control,
            )
            self.target_db.commit()

            origen = self.descargador.descargar_por_rango(
                control["fecha_desde"],
                control["fecha_hasta"],
            )
            total_origen = len(origen)
            resultado = self._procesar_dataframe(origen, id_control, total_origen)

            self.control_repository.actualizar_contadores(
                id_control,
                registros_origen=resultado.registros_origen,
                registros_insertados=resultado.registros_insertados,
                registros_duplicados=resultado.registros_duplicados,
                registros_invalidos=resultado.registros_invalidos,
            )
            if self.carga_repository is not None and id_carga is not None:
                self.carga_repository.finalizar_carga(
                    id_carga,
                    resultado.registros_origen,
                    resultado.registros_insertados,
                    resultado.registros_duplicados,
                    resultado.registros_invalidos,
                )
            self.control_repository.marcar_finalizado(id_control)
            self.log_repository.registrar(
                (
                    "Proceso finalizado. "
                    f"Origen: {resultado.registros_origen}, "
                    f"insertados: {resultado.registros_insertados}, "
                    f"duplicados: {resultado.registros_duplicados}, "
                    f"invalidos: {resultado.registros_invalidos}."
                ),
                id_control_descarga=id_control,
            )
            self.target_db.commit()
            return resultado
        except Exception as error:
            logging.exception("Fallo el procesamiento del control %s", id_control)
            self.target_db.rollback()
            self._registrar_error_control(id_control, error, id_carga)
            raise

    def _procesar_dataframe(
        self,
        origen: pd.DataFrame,
        id_control: int,
        total_origen: int,
    ) -> ResultadoProceso:
        if origen.empty:
            return ResultadoProceso(id_control, 0, 0, 0, 0)

        preparado = self._preparar_columnas_originales(origen)
        limpio = self.limpiador.limpiar_dataframe(preparado)
        homologado = self.homologador.homologar_dataframe(limpio)
        validos, invalidos = self.validador.obtener_registros_validos(homologado)
        con_clave = self.validador.agregar_clave_unica(validos)
        unicos, duplicados_lote = self.validador.eliminar_duplicados(con_clave)
        insertados, duplicados_bd = self.gestion_repository.insertar_lote(
            unicos.to_dict(orient="records"),
            id_control,
        )
        return ResultadoProceso(
            id_control=id_control,
            registros_origen=total_origen,
            registros_insertados=insertados,
            registros_duplicados=duplicados_lote + duplicados_bd,
            registros_invalidos=invalidos,
        )

    @staticmethod
    def _preparar_columnas_originales(df: pd.DataFrame) -> pd.DataFrame:
        preparado = df.copy()
        preparado["status_original"] = preparado.get("status")
        preparado["tipificacion_original"] = preparado.get("tipificacion")
        if "id_gestion_origen" not in preparado and "id" in preparado:
            preparado["id_gestion_origen"] = preparado["id"]
        return preparado

    def _registrar_error_control(
        self,
        id_control: int,
        error: Exception,
        id_carga: int | None,
    ) -> None:
        mensaje = str(error) or error.__class__.__name__
        try:
            self.control_repository.marcar_error(id_control, mensaje)
            if self.carga_repository is not None and id_carga is not None:
                self.carga_repository.finalizar_carga(
                    id_carga,
                    0,
                    0,
                    0,
                    0,
                    estado="ERROR",
                    mensaje_error=mensaje[:2000],
                )
            self.log_repository.registrar(
                "El procesamiento termino con error.",
                nivel="ERROR",
                id_control_descarga=id_control,
                detalle_error="".join(
                    traceback.format_exception_only(type(error), error)
                ).strip(),
            )
            self.target_db.commit()
        except Exception:
            self.target_db.rollback()
            logging.exception("No se pudo registrar el estado ERROR del control.")
