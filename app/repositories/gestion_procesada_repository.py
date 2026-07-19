from datetime import date, datetime
from decimal import Decimal
from typing import Any

import pandas as pd

from app.repositories.database import DatabaseConnection


class GestionProcesadaRepository:
    SQL_INSERTAR = """
        INSERT IGNORE INTO gestiones_procesadas (
            id_gestion_origen, fecha_gestion, dni, telefono,
            status_original, tipificacion_original,
            status_homologado, tipificacion_homologada,
            observacion, fecha_pago, monto_pago, nombre_asesor,
            clave_unica, id_control_descarga
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    def __init__(self, target_db: DatabaseConnection, batch_size: int = 1000):
        if batch_size <= 0:
            raise ValueError("batch_size debe ser mayor que cero.")
        self.target_db = target_db
        self.batch_size = batch_size

    def insertar_lote(
        self,
        gestiones: list[dict],
        id_control_descarga: int,
    ) -> tuple[int, int]:
        return self.insertar_ignorando_duplicados(gestiones, id_control_descarga)

    def insertar_ignorando_duplicados(
        self,
        gestiones: list[dict],
        id_control_descarga: int,
    ) -> tuple[int, int]:
        insertados = 0
        for inicio in range(0, len(gestiones), self.batch_size):
            lote = gestiones[inicio : inicio + self.batch_size]
            parametros = [
                self._a_parametros(gestion, id_control_descarga) for gestion in lote
            ]
            insertados += self.target_db.ejecutar_lote(self.SQL_INSERTAR, parametros)
        duplicados = len(gestiones) - insertados
        return insertados, duplicados

    def existe_clave_unica(self, clave_unica: str) -> bool:
        fila = self.target_db.obtener_uno(
            "SELECT 1 AS existe FROM gestiones_procesadas WHERE clave_unica = %s LIMIT 1",
            (clave_unica,),
        )
        return fila is not None

    def contar_por_rango(self, fecha_desde: datetime, fecha_hasta: datetime) -> int:
        fila = self.target_db.obtener_uno(
            """
            SELECT COUNT(*) AS total
            FROM gestiones_procesadas
            WHERE fecha_gestion >= %s AND fecha_gestion < %s
            """,
            (fecha_desde, fecha_hasta),
        )
        return int(fila["total"]) if fila else 0

    def obtener_por_rango(
        self,
        fecha_desde: datetime,
        fecha_hasta: datetime,
    ) -> list[dict]:
        return self.target_db.ejecutar_consulta(
            """
            SELECT *
            FROM gestiones_procesadas
            WHERE fecha_gestion >= %s AND fecha_gestion < %s
            ORDER BY fecha_gestion, id_procesado
            """,
            (fecha_desde, fecha_hasta),
        )

    @classmethod
    def _a_parametros(cls, gestion: dict, id_control: int) -> tuple:
        return (
            cls._valor(gestion.get("id_gestion_origen", gestion.get("id"))),
            cls._valor(gestion.get("fecha_gestion")),
            cls._valor(gestion.get("dni")),
            cls._valor(gestion.get("telefono")),
            cls._valor(gestion.get("status_original")),
            cls._valor(gestion.get("tipificacion_original")),
            cls._valor(gestion.get("status_homologado")),
            cls._valor(gestion.get("tipificacion_homologada")),
            cls._valor(gestion.get("observacion")),
            cls._valor(gestion.get("fecha_pago")),
            cls._valor(gestion.get("monto_pago")),
            cls._valor(gestion.get("nombre_asesor", gestion.get("nombre"))),
            cls._valor(gestion.get("clave_unica")),
            id_control,
        )

    @staticmethod
    def _valor(valor: Any) -> Any:
        if valor is None:
            return None
        try:
            if pd.isna(valor):
                return None
        except (TypeError, ValueError):
            pass
        if isinstance(valor, pd.Timestamp):
            return valor.to_pydatetime()
        if isinstance(valor, (datetime, date, Decimal, int, float, str)):
            return valor
        return valor
