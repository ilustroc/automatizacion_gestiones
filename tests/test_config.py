import os

import pytest

from app.config import (
    obtener_configuracion_source_db,
    obtener_configuracion_target_db,
)
from app.exceptions import ConfiguracionError


SOURCE_KEYS = {
    "SOURCE_DB_ENGINE": "mysql",
    "SOURCE_DB_HOST": "escall.example.com",
    "SOURCE_DB_PORT": "3306",
    "SOURCE_DB_NAME": "escarperu_software",
    "SOURCE_DB_USER": "lector",
    "SOURCE_DB_PASSWORD": "&Clave#{2026}?[x]+-@%",
    "SOURCE_DB_CONNECT_TIMEOUT": "15",
    "SOURCE_DB_READ_TIMEOUT": "120",
    "SOURCE_DB_WRITE_TIMEOUT": "120",
}

TARGET_KEYS = {
    "TARGET_DB_ENGINE": "mariadb",
    "TARGET_DB_HOST": "localhost",
    "TARGET_DB_PORT": "3306",
    "TARGET_DB_NAME": "automatizacion_gestiones",
    "TARGET_DB_USER": "local",
    "TARGET_DB_PASSWORD": "{local}&?#[]+-%",
    "TARGET_DB_CONNECT_TIMEOUT": "10",
    "TARGET_DB_READ_TIMEOUT": "60",
    "TARGET_DB_WRITE_TIMEOUT": "60",
}


def test_passwords_entre_comillas_y_caracteres_especiales(tmp_path, monkeypatch):
    ruta = tmp_path / ".env"
    contenido = "\n".join(
        f'{clave}="{valor}"' for clave, valor in {**SOURCE_KEYS, **TARGET_KEYS}.items()
    )
    ruta.write_text(contenido, encoding="utf-8")
    for clave in {**SOURCE_KEYS, **TARGET_KEYS}:
        monkeypatch.delenv(clave, raising=False)
    from app.config import cargar_configuracion

    cargar_configuracion(ruta, override=True)
    source = obtener_configuracion_source_db()
    target = obtener_configuracion_target_db()
    assert source.password == SOURCE_KEYS["SOURCE_DB_PASSWORD"]
    assert target.password == TARGET_KEYS["TARGET_DB_PASSWORD"]
    assert '"' not in source.password


def test_validacion_configuracion_origen(monkeypatch):
    for clave, valor in SOURCE_KEYS.items():
        monkeypatch.setenv(clave, valor)
    monkeypatch.setenv("SOURCE_DB_HOST", "")
    with pytest.raises(ConfiguracionError, match="SOURCE_DB_HOST"):
        obtener_configuracion_source_db()


def test_validacion_configuracion_destino(monkeypatch):
    for clave, valor in TARGET_KEYS.items():
        monkeypatch.setenv(clave, valor)
    monkeypatch.setenv("TARGET_DB_PORT", "no-es-puerto")
    with pytest.raises(ConfiguracionError, match="TARGET_DB_PORT"):
        obtener_configuracion_target_db()
