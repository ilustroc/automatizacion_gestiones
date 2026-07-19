from collections.abc import Iterable, Sequence
from contextlib import AbstractContextManager
from typing import Any

import pymysql
from pymysql.cursors import DictCursor

from app.config import (
    DatabaseConfig,
    SourceDatabaseConfig,
    TargetDatabaseConfig,
)
from app.exceptions import (
    SourceDatabaseConnectionError,
    StoredProcedureError,
    TargetDatabaseConnectionError,
)


SOURCE_CONNECTION_MESSAGE = (
    "No se pudo conectar al servidor origen ESCALL. Verifique que el puerto "
    "3306 esté habilitado, que la IP esté autorizada en Remote MySQL de cPanel, "
    "que el usuario tenga permisos y que el host sea correcto."
)
TARGET_CONNECTION_MESSAGE = (
    "No se pudo conectar a la base de datos local destino. Verifique que "
    "MySQL/MariaDB esté iniciado, que la base exista y que las credenciales "
    "locales sean correctas."
)


class DatabaseConnection(AbstractContextManager):
    """Conexion transaccional reutilizable para MySQL y MariaDB."""

    def __init__(self, config: DatabaseConfig):
        self.config = config
        self.connection: pymysql.connections.Connection | None = None

    def conectar(self) -> "DatabaseConnection":
        try:
            self.connection = pymysql.connect(
                host=self.config.host,
                port=self.config.port,
                user=self.config.user,
                password=self.config.password,
                database=self.config.name,
                charset=self.config.charset,
                cursorclass=DictCursor,
                autocommit=False,
                connect_timeout=self.config.connect_timeout,
                read_timeout=self.config.read_timeout,
                write_timeout=self.config.write_timeout,
            )
            return self
        except (pymysql.MySQLError, OSError) as error:
            if isinstance(self.config, SourceDatabaseConfig):
                raise SourceDatabaseConnectionError(SOURCE_CONNECTION_MESSAGE) from error
            raise TargetDatabaseConnectionError(TARGET_CONNECTION_MESSAGE) from error

    def cerrar(self) -> None:
        if self.connection is not None:
            self.connection.close()
            self.connection = None

    def commit(self) -> None:
        self._requerir_conexion().commit()

    def rollback(self) -> None:
        self._requerir_conexion().rollback()

    def cursor(self):
        return self._requerir_conexion().cursor()

    def probar_conexion(self) -> bool:
        fila = self.ejecutar_consulta("SELECT 1 AS conexion")
        return bool(fila and fila[0].get("conexion") == 1)

    def ejecutar_consulta(
        self,
        sql: str,
        parametros: Iterable[Any] | None = None,
    ) -> list[dict]:
        with self.cursor() as cursor:
            cursor.execute(sql, tuple(parametros or ()))
            return [dict(fila) for fila in cursor.fetchall()]

    def ejecutar_procedimiento(
        self,
        nombre: str,
        parametros: Iterable[Any] | None = None,
    ) -> list[dict]:
        try:
            with self.cursor() as cursor:
                cursor.callproc(nombre, tuple(parametros or ()))
                filas = [dict(fila) for fila in cursor.fetchall()]
                while cursor.nextset():
                    cursor.fetchall()
                return filas
        except pymysql.MySQLError as error:
            raise StoredProcedureError(
                f"No se pudo ejecutar el Stored Procedure {nombre}."
            ) from error

    def ejecutar_lote(
        self,
        sql: str,
        lote_parametros: Sequence[Sequence[Any]],
    ) -> int:
        if not lote_parametros:
            return 0
        with self.cursor() as cursor:
            return int(cursor.executemany(sql, lote_parametros))

    def ejecutar(
        self,
        sql: str,
        parametros: Iterable[Any] | None = None,
    ) -> int:
        with self.cursor() as cursor:
            return int(cursor.execute(sql, tuple(parametros or ())))

    def ejecutar_y_obtener_id(
        self,
        sql: str,
        parametros: Iterable[Any] | None = None,
    ) -> int:
        with self.cursor() as cursor:
            cursor.execute(sql, tuple(parametros or ()))
            return int(cursor.lastrowid)

    def obtener_todos(
        self,
        sql: str,
        parametros: Iterable[Any] | None = None,
    ) -> list[dict]:
        return self.ejecutar_consulta(sql, parametros)

    def obtener_uno(
        self,
        sql: str,
        parametros: Iterable[Any] | None = None,
    ) -> dict | None:
        filas = self.ejecutar_consulta(sql, parametros)
        return filas[0] if filas else None

    def llamar_procedimiento(
        self,
        nombre: str,
        parametros: Iterable[Any] | None = None,
    ) -> list[dict]:
        return self.ejecutar_procedimiento(nombre, parametros)

    def confirmar(self) -> None:
        self.commit()

    def revertir(self) -> None:
        self.rollback()

    def __enter__(self) -> "DatabaseConnection":
        return self.conectar()

    def __exit__(self, exc_type, exc_value, traceback) -> bool:
        try:
            if self.connection is not None:
                if exc_type is None:
                    self.commit()
                else:
                    self.rollback()
        finally:
            self.cerrar()
        return False

    def _requerir_conexion(self) -> pymysql.connections.Connection:
        if self.connection is None:
            raise RuntimeError("La conexion a la base de datos no esta abierta.")
        return self.connection


# Alias compatible con la primera version del proyecto.
Database = DatabaseConnection
