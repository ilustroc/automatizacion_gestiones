from collections.abc import Iterable
from typing import Any

import psycopg2
from psycopg2.extras import RealDictCursor

from app.config import DatabaseConfig


class Database:
    """Conexion sencilla a PostgreSQL/Supabase."""

    def __init__(self, config: DatabaseConfig):
        self.config = config
        self.connection = None

    def conectar(self) -> None:
        self.connection = psycopg2.connect(
            host=self.config.host,
            port=self.config.port,
            dbname=self.config.name,
            user=self.config.user,
            password=self.config.password,
            sslmode=self.config.sslmode,
        )

    def cerrar(self) -> None:
        if self.connection:
            self.connection.close()

    def confirmar(self) -> None:
        if self.connection:
            self.connection.commit()

    def revertir(self) -> None:
        if self.connection:
            self.connection.rollback()

    def obtener_todos(self, sql: str, parametros: Iterable[Any] | None = None) -> list[dict]:
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(sql, parametros)
            return [dict(fila) for fila in cursor.fetchall()]

    def obtener_uno(self, sql: str, parametros: Iterable[Any] | None = None) -> dict | None:
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(sql, parametros)
            fila = cursor.fetchone()
            return dict(fila) if fila else None

    def ejecutar(self, sql: str, parametros: Iterable[Any] | None = None) -> int:
        with self.connection.cursor() as cursor:
            cursor.execute(sql, parametros)
            return cursor.rowcount

    def insertar_y_retornar(
        self, sql: str, parametros: Iterable[Any] | None = None
    ) -> dict | None:
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(sql, parametros)
            fila = cursor.fetchone()
            return dict(fila) if fila else None

