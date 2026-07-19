import hashlib

import pandas as pd
import pytest

from app.exceptions import ValidacionGestionError
from app.services.validador_service import ValidadorService


def _registro_valido() -> dict:
    return {
        "id_gestion_origen": 1,
        "dni": "16785157",
        "telefono": "991956360",
        "fecha_gestion": pd.Timestamp("2024-01-26 18:36:34"),
        "status_homologado": "INDIRECTO",
        "tipificacion_homologada": "ILOCALIZADO",
    }


def test_clave_unica_es_sha256_estable_de_64_caracteres():
    validador = ValidadorService()
    resultado = validador.agregar_clave_unica(pd.DataFrame([_registro_valido()]))
    base = "16785157|991956360|2024-01-26 18:36:34|INDIRECTO|ILOCALIZADO"
    esperado = hashlib.sha256(base.encode("utf-8")).hexdigest()
    assert resultado.loc[0, "clave_unica"] == esperado
    assert len(esperado) == 64


def test_eliminacion_duplicados_usa_hash():
    validador = ValidadorService()
    df = validador.agregar_clave_unica(
        pd.DataFrame([_registro_valido(), _registro_valido()])
    )
    unicos, duplicados = validador.eliminar_duplicados(df)
    assert len(unicos) == 1
    assert duplicados == 1


def test_validacion_descarta_id_y_dni_invalidos():
    valido = _registro_valido()
    invalido = {**_registro_valido(), "id_gestion_origen": None, "dni": ""}
    validos, descartados = ValidadorService().obtener_registros_validos(
        pd.DataFrame([valido, invalido])
    )
    assert len(validos) == 1
    assert descartados == 1


def test_validacion_reporta_columna_obligatoria_faltante():
    with pytest.raises(ValidacionGestionError, match="id_gestion_origen"):
        ValidadorService().obtener_registros_validos(
            pd.DataFrame([{"dni": "12345678"}])
        )
