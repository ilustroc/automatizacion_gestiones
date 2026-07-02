from datetime import date, datetime
from decimal import Decimal
from typing import Any

import pandas as pd

from app.repositories.database import Database


class GestionRepository:
    def __init__(self, db: Database):
        self.db = db

    def obtener_gestiones_origen(self, consulta_sql: str | None = None) -> list[dict]:
        sql = consulta_sql or """
            SELECT
                id_cartera,
                id_usuario,
                fecha_gestion,
                dni,
                telefono,
                status,
                tipificacion,
                observacion,
                fecha_pago,
                monto_pago,
                nombre
            FROM gestiones
            ORDER BY creado_en DESC
            LIMIT 100
        """
        return self.db.obtener_todos(sql)

    def insertar_gestiones(self, gestiones: list[dict], id_carga: int) -> tuple[int, int]:
        insertados = 0
        duplicados = 0

        for gestion in gestiones:
            fila = self.db.insertar_y_retornar(
                """
                INSERT INTO gestiones (
                    id_carga,
                    id_cartera,
                    id_usuario,
                    fecha_gestion,
                    dni,
                    telefono,
                    status,
                    tipificacion,
                    observacion,
                    fecha_pago,
                    monto_pago,
                    nombre,
                    clave_unica
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (clave_unica) DO NOTHING
                RETURNING id_gestion
                """,
                (
                    id_carga,
                    self._valor(gestion.get("id_cartera")),
                    self._valor(gestion.get("id_usuario")),
                    self._valor(gestion.get("fecha_gestion")),
                    self._valor(gestion.get("dni")),
                    self._valor(gestion.get("telefono")),
                    self._valor(gestion.get("status")),
                    self._valor(gestion.get("tipificacion")),
                    self._valor(gestion.get("observacion")),
                    self._valor(gestion.get("fecha_pago")),
                    self._valor(gestion.get("monto_pago")),
                    self._valor(gestion.get("nombre")),
                    self._valor(gestion.get("clave_unica")),
                ),
            )

            if fila:
                insertados += 1
            else:
                duplicados += 1

        return insertados, duplicados

    def existe_clave_unica(self, clave_unica: str) -> bool:
        fila = self.db.obtener_uno(
            "SELECT 1 AS existe FROM gestiones WHERE clave_unica = %s",
            (clave_unica,),
        )
        return fila is not None

    def _valor(self, valor: Any) -> Any:
        if valor is None:
            return None
        if isinstance(valor, float) and pd.isna(valor):
            return None
        if pd.isna(valor) and not isinstance(valor, (str, bytes)):
            return None
        if isinstance(valor, pd.Timestamp):
            return valor.to_pydatetime()
        if isinstance(valor, (datetime, date, Decimal, int, str)):
            return valor
        return valor

