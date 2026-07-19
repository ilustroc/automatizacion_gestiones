from datetime import date
from html import escape
from pathlib import Path

import pandas as pd

from app.exceptions import ReporteError
from app.repositories.reporte_repository import ReporteRepository


class ReportePromesasService:
    tipo_reporte = "PROMESAS"
    asunto = "Alerta de promesas de pago"

    def __init__(self, reporte_repository: ReporteRepository):
        self.reporte_repository = reporte_repository

    def obtener_datos(self) -> list[dict]:
        return self.reporte_repository.obtener_alerta_promesas_pago()

    def crear_asunto(self, fecha: date | None = None) -> str:
        return f"Alerta de promesas de pago - {(fecha or date.today()).isoformat()}"

    def generar_html(self, datos: list[dict]) -> str:
        conteos = {
            nivel: sum(1 for fila in datos if fila.get("nivel_alerta") == nivel)
            for nivel in ("VENCIDA", "VENCE HOY", "VENCE MAÑANA")
        }
        filas = "".join(
            "<tr>"
            f"<td>{escape(str(fila.get('dni', '') or ''))}</td>"
            f"<td>{escape(str(fila.get('telefono', '') or ''))}</td>"
            f"<td>{escape(str(fila.get('nombre_asesor', '') or ''))}</td>"
            f"<td>{escape(str(fila.get('fecha_pago', '') or ''))}</td>"
            f"<td>{escape(str(fila.get('monto_pago', '') or ''))}</td>"
            f"<td>{escape(str(fila.get('tipificacion_homologada', '') or ''))}</td>"
            f"<td>{escape(str(fila.get('observacion', '') or ''))}</td>"
            f"<td>{escape(str(fila.get('nivel_alerta', '') or ''))}</td>"
            "</tr>"
            for fila in datos
        )
        return f"""
        <h2>Alerta de promesas de pago</h2>
        <p>Vencidas: {conteos['VENCIDA']} | Vencen hoy: {conteos['VENCE HOY']} |
        Vencen mañana: {conteos['VENCE MAÑANA']}</p>
        <table border="1" cellpadding="6" cellspacing="0">
          <tr><th>DNI</th><th>Teléfono</th><th>Asesor</th><th>Fecha de promesa</th>
          <th>Monto</th><th>Tipificación</th><th>Observación</th><th>Alerta</th></tr>
          {filas}
        </table>
        """

    def exportar_excel(self, datos: list[dict], ruta: Path) -> Path:
        try:
            ruta.parent.mkdir(parents=True, exist_ok=True)
            pd.DataFrame(datos).to_excel(ruta, index=False, engine="openpyxl")
            return ruta
        except Exception as error:
            raise ReporteError("No se pudo generar el Excel de promesas.") from error
