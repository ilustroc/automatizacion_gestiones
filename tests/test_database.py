import pytest

from app.config import SourceDatabaseConfig, TargetDatabaseConfig
from app.exceptions import (
    SourceDatabaseConnectionError,
    TargetDatabaseConnectionError,
)
from app.repositories.database import DatabaseConnection


def _source_config():
    return SourceDatabaseConfig("mysql", "source", 3306, "origen", "lector", "secreto")


def _target_config():
    return TargetDatabaseConfig("mysql", "localhost", 3306, "destino", "local", "secreto")


def test_error_conexion_origen_muestra_orientacion_sin_password(monkeypatch):
    monkeypatch.setattr("pymysql.connect", lambda **kwargs: (_ for _ in ()).throw(OSError("timeout")))
    with pytest.raises(SourceDatabaseConnectionError, match="Remote MySQL") as error:
        DatabaseConnection(_source_config()).conectar()
    assert "secreto" not in str(error.value)


def test_error_conexion_destino_es_diferenciado(monkeypatch):
    monkeypatch.setattr("pymysql.connect", lambda **kwargs: (_ for _ in ()).throw(OSError("offline")))
    with pytest.raises(TargetDatabaseConnectionError, match="base de datos local"):
        DatabaseConnection(_target_config()).conectar()
