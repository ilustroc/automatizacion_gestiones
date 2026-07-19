from pathlib import Path

import pandas as pd


class ReporteService:
    """Utilidades compartidas para reportes."""

    def exportar_excel(self, datos: list[dict], ruta_salida: Path) -> None:
        ruta_salida.parent.mkdir(parents=True, exist_ok=True)
        pd.DataFrame(datos).to_excel(ruta_salida, index=False, engine="openpyxl")

    def crear_resumen_operativo(
        self,
        leidos: int,
        insertados: int,
        duplicados: int,
        descartados: int,
    ) -> str:
        return (
            "Resumen de ejecucion\n"
            f"- Registros leidos: {leidos}\n"
            f"- Registros insertados: {insertados}\n"
            f"- Registros duplicados: {duplicados}\n"
            f"- Registros descartados: {descartados}"
        )
