from collections import Counter
from datetime import date, datetime
from html import escape
from pathlib import Path

import pandas as pd

from app.exceptions import ReporteError
from app.repositories.reporte_repository import ReporteRepository


class ReporteImpulseService:
    tipo_reporte = "IMPULSE"
    asunto = "Reporte de gestiones realizadas - Impulse"

    def __init__(self, reporte_repository: ReporteRepository):
        self.reporte_repository = reporte_repository

    def obtener_datos(
        self,
        fecha_desde: datetime | None = None,
        fecha_hasta: datetime | None = None,
    ) -> list[dict]:
        if fecha_desde is None or fecha_hasta is None:
            return self.reporte_repository.obtener_reporte_impulse()
        return self.reporte_repository.obtener_reporte_impulse(fecha_desde, fecha_hasta)

    def crear_asunto(self, fecha: date | None = None) -> str:
        return (
            "Reporte de gestiones realizadas - Impulse - "
            f"{(fecha or date.today()).isoformat()}"
        )

    def generar_html(
        self,
        datos: list[dict],
        periodo: str | None = None,
    ) -> str:
        estados = Counter(str(fila.get("status_homologado", "")) for fila in datos)
        tipificaciones = Counter(
            str(fila.get("tipificacion_homologada", "")) for fila in datos
        )
        clientes = len({fila.get("dni") for fila in datos if fila.get("dni")})
        resumen_tipificaciones = "".join(
            f"<li>{escape(nombre)}: {total}</li>"
            for nombre, total in sorted(tipificaciones.items())
        )
        filas = "".join(
            "<tr>"
            f"<td>{escape(str(fila.get('fecha_gestion', '') or ''))}</td>"
            f"<td>{escape(str(fila.get('dni', '') or ''))}</td>"
            f"<td>{escape(str(fila.get('telefono', '') or ''))}</td>"
            f"<td>{escape(str(fila.get('status_homologado', '') or ''))}</td>"
            f"<td>{escape(str(fila.get('tipificacion_homologada', '') or ''))}</td>"
            f"<td>{escape(str(fila.get('observacion', '') or ''))}</td>"
            f"<td>{escape(str(fila.get('fecha_pago', '') or ''))}</td>"
            f"<td>{escape(str(fila.get('monto_pago', '') or ''))}</td>"
            f"<td>{escape(str(fila.get('nombre_asesor', '') or ''))}</td>"
            "</tr>"
            for fila in datos
        )
        return f"""
        <h2>Reporte de gestiones realizadas - Impulse</h2>
        <p>Periodo procesado: {escape(periodo or 'periodo consultado')}</p>
        <p>Total: {len(datos)} | Clientes únicos: {clientes} |
        Directo: {estados['DIRECTO']} | Indirecto: {estados['INDIRECTO']} |
        No contacto: {estados['NO CONTACTO']}</p>
        <h3>Resumen por tipificación</h3><ul>{resumen_tipificaciones}</ul>
        <table border="1" cellpadding="6" cellspacing="0">
          <tr><th>Fecha</th><th>DNI</th><th>Teléfono</th><th>Status</th>
          <th>Tipificación</th><th>Observación</th><th>Fecha pago</th>
          <th>Monto</th><th>Asesor</th></tr>{filas}
        </table>
        """

    def exportar_excel(self, datos: list[dict], ruta: Path) -> Path:
        try:
            ruta.parent.mkdir(parents=True, exist_ok=True)
            pd.DataFrame(datos).to_excel(ruta, index=False, engine="openpyxl")
            return ruta
        except Exception as error:
            raise ReporteError("No se pudo generar el Excel de Impulse.") from error
