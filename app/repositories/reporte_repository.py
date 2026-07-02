from datetime import date

from app.repositories.database import Database


class ReporteRepository:
    def __init__(self, db: Database):
        self.db = db

    def consultar_resumen_gestiones(self) -> list[dict]:
        return self.db.obtener_todos(
            """
            SELECT fecha, status, tipificacion, total_gestiones, clientes_unicos, monto_total
            FROM vw_resumen_gestiones
            ORDER BY fecha DESC, status, tipificacion
            """
        )

    def crear_reporte(
        self,
        tipo_reporte: str,
        periodo_desde: date,
        periodo_hasta: date,
        ruta_archivo: str | None = None,
    ) -> int:
        fila = self.db.insertar_y_retornar(
            """
            INSERT INTO reportes (
                tipo_reporte,
                periodo_desde,
                periodo_hasta,
                ruta_archivo,
                estado
            )
            VALUES (%s, %s, %s, %s, 'GENERADO')
            RETURNING id_reporte
            """,
            (tipo_reporte, periodo_desde, periodo_hasta, ruta_archivo),
        )
        return int(fila["id_reporte"])

