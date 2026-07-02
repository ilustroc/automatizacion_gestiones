from pathlib import Path

import pandas as pd

from app.repositories.reporte_repository import ReporteRepository


class ReporteService:
    def __init__(self, reporte_repository: ReporteRepository | None = None):
        self.reporte_repository = reporte_repository

    def obtener_resumen_desde_bd(self) -> list[dict]:
        if not self.reporte_repository:
            raise ValueError("ReporteService requiere un ReporteRepository.")
        return self.reporte_repository.consultar_resumen_gestiones()

    def exportar_excel(self, df: pd.DataFrame, ruta_salida: Path) -> None:
        ruta_salida.parent.mkdir(parents=True, exist_ok=True)
        df.to_excel(ruta_salida, index=False, engine="openpyxl")

    def formatear_resumen_bd(self, resumen: list[dict]) -> str:
        if not resumen:
            return "Resumen desde vw_resumen_gestiones: no hay registros para mostrar."

        lineas = ["Resumen desde vw_resumen_gestiones"]
        for fila in resumen[:10]:
            lineas.append(
                "- {fecha} | {status} | {tipificacion}: {total} gestiones, "
                "{clientes} clientes, monto {monto}".format(
                    fecha=fila.get("fecha"),
                    status=fila.get("status"),
                    tipificacion=fila.get("tipificacion"),
                    total=fila.get("total_gestiones"),
                    clientes=fila.get("clientes_unicos"),
                    monto=fila.get("monto_total"),
                )
            )
        return "\n".join(lineas)

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
