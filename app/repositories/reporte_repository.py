from datetime import datetime
from pathlib import Path

from app.repositories.database import DatabaseConnection


class ReporteRepository:
    def __init__(self, target_db: DatabaseConnection):
        self.target_db = target_db

    def obtener_alerta_promesas_pago(self) -> list[dict]:
        return self.target_db.ejecutar_consulta(
            """
            SELECT *
            FROM vw_alerta_promesas_pago
            WHERE nivel_alerta IN ('VENCIDA', 'VENCE HOY', 'VENCE MAÑANA')
            ORDER BY fecha_pago, nombre_asesor, dni
            """
        )

    def obtener_reporte_impulse(
        self,
        fecha_desde: datetime | None = None,
        fecha_hasta: datetime | None = None,
    ) -> list[dict]:
        sql = "SELECT * FROM vw_reporte_impulse_gestiones"
        parametros: tuple = ()
        if fecha_desde is not None and fecha_hasta is not None:
            sql += " WHERE fecha_gestion >= %s AND fecha_gestion < %s"
            parametros = (fecha_desde, fecha_hasta)
        sql += " ORDER BY fecha_gestion, dni"
        return self.target_db.ejecutar_consulta(sql, parametros)

    def obtener_reporte_gerencia_asesores(
        self,
        fecha_desde: datetime | None = None,
        fecha_hasta: datetime | None = None,
    ) -> list[dict]:
        sql = "SELECT * FROM vw_reporte_gerencia_asesores_dia"
        parametros: tuple = ()
        if fecha_desde is not None and fecha_hasta is not None:
            sql += " WHERE fecha >= DATE(%s) AND fecha < DATE(%s)"
            parametros = (fecha_desde, fecha_hasta)
        sql += " ORDER BY fecha, total_gestiones DESC, nombre_asesor"
        return self.target_db.ejecutar_consulta(sql, parametros)

    def registrar_reporte(
        self,
        tipo_reporte: str,
        fecha_desde: datetime | None,
        fecha_hasta: datetime | None,
        ruta_archivo: Path | None,
    ) -> int:
        return self.target_db.ejecutar_y_obtener_id(
            """
            INSERT INTO reportes (
                tipo_reporte, fecha_desde, fecha_hasta, ruta_archivo, estado
            )
            VALUES (%s, %s, %s, %s, 'GENERADO')
            """,
            (
                tipo_reporte,
                fecha_desde,
                fecha_hasta,
                str(ruta_archivo) if ruta_archivo else None,
            ),
        )
