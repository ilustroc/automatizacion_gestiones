import logging

import pandas as pd

from app.config import (
    INPUT_FILE,
    OUTPUT_FILE,
    cargar_configuracion,
    configurar_logging,
)
from app.repositories.gestion_repository import GestionRepository
from app.services.homologador_service import HomologadorService
from app.services.limpiador_service import LimpiadorService
from app.services.reporte_service import ReporteService
from app.services.validador_service import ValidadorService


def main() -> None:
    cargar_configuracion()
    configurar_logging()

    logging.info("Inicio del proceso de gestiones de cobranza")

    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"No existe el archivo de entrada: {INPUT_FILE}")

    df = pd.read_csv(INPUT_FILE, dtype=str, encoding="utf-8")
    total_leidos = len(df)
    logging.info("Registros leidos: %s", total_leidos)

    validador = ValidadorService()
    limpiador = LimpiadorService()
    homologador = HomologadorService()
    reporte = ReporteService()
    repositorio = GestionRepository()

    validador.validar_columnas(df)
    df_limpio = limpiador.limpiar_dataframe(df)
    df_homologado = homologador.homologar_dataframe(df_limpio)
    df_final, duplicados_eliminados = validador.eliminar_duplicados(df_homologado)

    reporte.exportar_excel(df_final, OUTPUT_FILE)
    repositorio.guardar_gestiones(df_final)

    resumen = reporte.crear_resumen(
        total_leidos=total_leidos,
        total_limpios=len(df_final),
        duplicados_eliminados=duplicados_eliminados,
        ruta_salida=OUTPUT_FILE,
    )

    logging.info("Registros finales: %s", len(df_final))
    logging.info("Duplicados eliminados: %s", duplicados_eliminados)
    logging.info("Archivo generado: %s", OUTPUT_FILE)
    print(resumen)


if __name__ == "__main__":
    main()

