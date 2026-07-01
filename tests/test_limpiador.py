from app.services.limpiador_service import LimpiadorService


def test_limpieza_dni_deja_solo_numeros():
    limpiador = LimpiadorService()

    resultado = limpiador.limpiar_dni("DNI 12.345.678")

    assert resultado == "12345678"


def test_limpieza_telefono_deja_solo_numeros():
    limpiador = LimpiadorService()

    resultado = limpiador.limpiar_telefono("(01) 999-888-777")

    assert resultado == "01999888777"

