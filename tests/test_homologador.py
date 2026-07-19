from app.services.homologador_service import HomologadorService


def test_homologacion_status_definidos():
    homologador = HomologadorService()
    assert homologador.homologar_status("CD") == "DIRECTO"
    assert homologador.homologar_status("contacto indirecto") == "INDIRECTO"
    assert homologador.homologar_status("ILOCALIZADO") == "NO CONTACTO"
    assert homologador.homologar_status("valor desconocido") == "SIN GESTIÓN"


def test_homologacion_tipificaciones_y_regla_configurable():
    homologador = HomologadorService({"acuerdo especial": "ACUERDO"})
    assert homologador.homologar_tipificacion("PDP") == "PROMESA DE PAGO"
    assert homologador.homologar_tipificacion("numero incorrecto") == "NÚMERO INCORRECTO"
    assert homologador.homologar_tipificacion("acuerdo especial") == "ACUERDO"
