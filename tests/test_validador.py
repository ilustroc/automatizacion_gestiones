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

