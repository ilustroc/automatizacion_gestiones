from app.services.homologador_service import HomologadorService


def test_homologacion_status_contacto_directo():
    homologador = HomologadorService()

    resultado = homologador.homologar_status("CD")

    assert resultado == "DIRECTO"


def test_homologacion_status_ilocalizado():
    homologador = HomologadorService()

    resultado = homologador.homologar_status("ILOCALIZADO")

    assert resultado == "NO CONTACTO"


def test_homologacion_tipificacion_promesa():
    homologador = HomologadorService()

    resultado = homologador.homologar_tipificacion("PDP")

    assert resultado == "PROMESA DE PAGO"


def test_homologacion_tipificacion_numero_incorrecto_con_acento():
    homologador = HomologadorService()

    resultado = homologador.homologar_tipificacion("NÚMERO INCORRECTO")

    assert resultado == "NÚMERO INCORRECTO"

