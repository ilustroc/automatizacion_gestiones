from decimal import Decimal

import pandas as pd

from app.services.limpiador_service import LimpiadorService


def test_limpieza_dni_deja_solo_numeros_y_conserva_ceros():
    limpiador = LimpiadorService()
    assert limpiador.limpiar_dni("DNI 00.123.456") == "00123456"


def test_limpieza_telefono_deja_solo_numeros():
    limpiador = LimpiadorService()
    assert limpiador.limpiar_telefono("(01) 999-888-777") == "01999888777"


def test_dni_numerico_no_agrega_cero_por_decimal():
    assert LimpiadorService().limpiar_dni(12345678.0) == "12345678"


def test_limpieza_dataframe_convierte_fecha_monto_y_nulos():
    df = pd.DataFrame(
        [
            {
                "id": 7,
                "fecha_gestion": "18/07/2026 08:30:00",
                "dni": "0012-3456",
                "telefono": None,
                "status": "  contacto   directo ",
                "tipificacion": " PDP ",
                "observacion": None,
                "fecha_pago": "19/07/2026",
                "monto_pago": "1.234,50",
                "nombre": " Ana   Perez ",
            }
        ]
    )
    fila = LimpiadorService().limpiar_dataframe(df).iloc[0]
    assert fila["id_gestion_origen"] == 7
    assert fila["dni"] == "00123456"
    assert fila["telefono"] is None
    assert fila["monto_pago"] == Decimal("1234.50")
    assert fila["nombre_asesor"] == "Ana Perez"
