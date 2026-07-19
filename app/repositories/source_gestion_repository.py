from collections.abc import Iterator
from datetime import datetime

from app.repositories.database import DatabaseConnection


class SourceGestionRepository:
    """Acceso de solo lectura a las gestiones del servidor ESCALL."""

    PROCEDIMIENTO = "sp_descargar_gestiones_rango"

    def __init__(self, source_db: DatabaseConnection):
        self.source_db = source_db

    def obtener_gestiones_por_rango(
        self,
        fecha_desde: datetime,
        fecha_hasta: datetime,
    ) -> list[dict]:
        self._validar_rango(fecha_desde, fecha_hasta)
        return self.source_db.ejecutar_procedimiento(
            self.PROCEDIMIENTO,
            (fecha_desde, fecha_hasta),
        )

    def obtener_gestiones_por_lotes(
        self,
        fecha_desde: datetime,
        fecha_hasta: datetime,
        batch_size: int,
    ) -> Iterator[list[dict]]:
        if batch_size <= 0:
            raise ValueError("batch_size debe ser mayor que cero.")
        registros = self.obtener_gestiones_por_rango(fecha_desde, fecha_hasta)
        for inicio in range(0, len(registros), batch_size):
            yield registros[inicio : inicio + batch_size]

    def contar_gestiones_por_rango(
        self,
        fecha_desde: datetime,
        fecha_hasta: datetime,
    ) -> int:
        self._validar_rango(fecha_desde, fecha_hasta)
        fila = self.source_db.obtener_uno(
            """
            SELECT COUNT(*) AS total
            FROM gestiones
            WHERE fecha_gestion >= %s AND fecha_gestion < %s
            """,
            (fecha_desde, fecha_hasta),
        )
        return int(fila["total"]) if fila else 0

    def probar_stored_procedure(self, instante: datetime | None = None) -> bool:
        referencia = instante or datetime.now()
        self.source_db.ejecutar_procedimiento(
            self.PROCEDIMIENTO,
            (referencia, referencia),
        )
        return True

    @staticmethod
    def _validar_rango(fecha_desde: datetime, fecha_hasta: datetime) -> None:
        if fecha_hasta <= fecha_desde:
            raise ValueError("fecha_hasta debe ser mayor que fecha_desde.")
