import pandas as pd

from app.services.validador_service import ValidadorService


def test_eliminacion_duplicados_por_clave_compuesta():
    validador = ValidadorService()
    df = pd.DataFrame(
        [
            {
                "dni": "12345678",
                "telefono": "987654321",
                "fecha_gestion": pd.Timestamp("2026-06-01 09:15"),
                "status": "DIRECTO",
                "tipificacion": "PROMESA DE PAGO",
                "observacion": "Primera gestion",
            },
            {
                "dni": "12345678",
                "telefono": "987654321",
                "fecha_gestion": pd.Timestamp("2026-06-01 09:15"),
                "status": "DIRECTO",
                "tipificacion": "PROMESA DE PAGO",
                "observacion": "Gestion repetida",
            },
        ]
    )

    df_sin_duplicados, duplicados = validador.eliminar_duplicados(df)

    assert len(df_sin_duplicados) == 1
    assert duplicados == 1


def test_agregar_clave_unica_para_base_de_datos():
    validador = ValidadorService()
    df = pd.DataFrame(
        [
            {
                "dni": "16785157",
                "telefono": "991956360",
                "fecha_gestion": pd.Timestamp("2024-01-26 18:36:34"),
                "status": "INDIRECTO",
                "tipificacion": "ILOCALIZADO",
            }
        ]
    )

    resultado = validador.agregar_clave_unica(df)

    assert (
        resultado.loc[0, "clave_unica"]
        == "16785157|991956360|2024-01-26 18:36:34|INDIRECTO|ILOCALIZADO"
    )


def test_validacion_descarta_registros_sin_campos_obligatorios():
    validador = ValidadorService()
    df = pd.DataFrame(
        [
            {
                "fecha_gestion": pd.Timestamp("2026-06-01 09:15"),
                "dni": "12345678",
                "status": "DIRECTO",
                "tipificacion": "PROMESA DE PAGO",
            },
            {
                "fecha_gestion": pd.Timestamp("2026-06-01 10:00"),
                "dni": "",
                "status": "DIRECTO",
                "tipificacion": "PROMESA DE PAGO",
            },
        ]
    )

    validos, descartados = validador.obtener_registros_validos(df)

    assert len(validos) == 1
    assert descartados == 1
