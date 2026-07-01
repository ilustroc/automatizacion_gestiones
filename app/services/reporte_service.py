from pathlib import Path

import pandas as pd


class ReporteService:
    def exportar_excel(self, df: pd.DataFrame, ruta_salida: Path) -> None:
        ruta_salida.parent.mkdir(parents=True, exist_ok=True)
        df.to_excel(ruta_salida, index=False, engine="openpyxl")

    def crear_resumen(
        self,
        total_leidos: int,
        total_limpios: int,
        duplicados_eliminados: int,
        ruta_salida: Path,
    ) -> str:
        return (
            "Resumen de ejecucion\n"
            f"- Total de registros leidos: {total_leidos}\n"
            f"- Total de registros limpios: {total_limpios}\n"
            f"- Total de duplicados eliminados: {duplicados_eliminados}\n"
            f"- Archivo generado: {ruta_salida}"
        )

