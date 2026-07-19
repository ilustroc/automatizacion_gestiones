from datetime import date, datetime
from html import escape
from pathlib import Path

import pandas as pd

from app.exceptions import ReporteError
from app.repositories.reporte_repository import ReporteRepository


class ReporteGerenciaService:
    tipo_reporte = "GERENCIA"
    asunto = "Reporte gerencial de productividad de asesores"

    def __init__(self, reporte_repository: ReporteRepository):
        self.reporte_repository = reporte_repository

    def obtener_datos(
        self,
        fecha_desde: datetime | None = None,
        fecha_hasta: datetime | None = None,
    ) -> list[dict]:
        if fecha_desde is None or fecha_hasta is None:
            datos = self.reporte_repository.obtener_reporte_gerencia_asesores()
        else:
            datos = self.reporte_repository.obtener_reporte_gerencia_asesores(
                fecha_desde, fecha_hasta
            )
        return self._agregar_ranking(datos)

    def crear_asunto(self, fecha: date | None = None) -> str:
        return (
            "Reporte gerencial de productividad de asesores - "
            f"{(fecha or date.today()).isoformat()}"
        )

    def generar_html(self, datos: list[dict]) -> str:
        filas = "".join(
            "<tr>"
            f"<td>{escape(str(fila.get('fecha', '') or ''))}</td>"
            f"<td>{escape(str(fila.get('nombre_asesor', '') or ''))}</td>"
            f"<td>{fila.get('total_gestiones', 0)}</td>"
            f"<td>{fila.get('contactos_directos', 0)}</td>"
            f"<td>{fila.get('contactos_indirectos', 0)}</td>"
            f"<td>{fila.get('no_contactos', 0)}</td>"
            f"<td>{fila.get('total_promesas', 0)}</td>"
            f"<td>{fila.get('monto_prometido', 0)}</td>"
            f"<td>{fila.get('clientes_unicos', 0)}</td>"
            f"<td>{fila.get('ranking_diario', '')}</td>"
            "</tr>"
            for fila in datos
        )
        return f"""
        <h2>Reporte gerencial de productividad de asesores</h2>
        <table border="1" cellpadding="6" cellspacing="0">
          <tr><th>Fecha</th><th>Asesor</th><th>Total</th><th>Directo</th>
          <th>Indirecto</th><th>No contacto</th><th>Promesas</th>
          <th>Monto prometido</th><th>Clientes únicos</th><th>Ranking</th></tr>
          {filas}
        </table>
        """

    def exportar_excel(self, datos: list[dict], ruta: Path) -> Path:
        try:
            ruta.parent.mkdir(parents=True, exist_ok=True)
            pd.DataFrame(datos).to_excel(ruta, index=False, engine="openpyxl")
            return ruta
        except Exception as error:
            raise ReporteError("No se pudo generar el Excel gerencial.") from error

    @staticmethod
    def _agregar_ranking(datos: list[dict]) -> list[dict]:
        resultado = [dict(fila) for fila in datos]
        fechas = {fila.get("fecha") for fila in resultado}
        for fecha in fechas:
            filas_fecha = [fila for fila in resultado if fila.get("fecha") == fecha]
            valores = sorted(
                {int(fila.get("total_gestiones", 0)) for fila in filas_fecha},
                reverse=True,
            )
            ranking = {total: indice + 1 for indice, total in enumerate(valores)}
            for fila in filas_fecha:
                fila["ranking_diario"] = ranking[int(fila.get("total_gestiones", 0))]
        return resultado
