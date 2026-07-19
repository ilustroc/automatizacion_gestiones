from datetime import datetime

import pytest

from app.repositories.control_descarga_repository import ControlDescargaRepository
from jobs.job_descarga_horaria import calcular_rango_horario


class FakeTarget:
    def obtener_uno(self, sql, parametros=None):
        return {"id_control": 8, "estado": "PENDIENTE"}


def test_control_rechaza_rango_invalido():
    with pytest.raises(ValueError, match="mayor"):
        ControlDescargaRepository._validar_rango(
            datetime(2026, 7, 18, 9), datetime(2026, 7, 18, 9)
        )


def test_control_pendiente_se_consulta_en_vista_local():
    resultado = ControlDescargaRepository(FakeTarget()).obtener_pendiente()
    assert resultado["id_control"] == 8
    assert resultado["estado"] == "PENDIENTE"


def test_job_horario_usa_ultima_hora_cerrada():
    desde, hasta = calcular_rango_horario(datetime(2026, 7, 18, 18, 5, 42))
    assert desde == datetime(2026, 7, 18, 17, 0, 0)
    assert hasta == datetime(2026, 7, 18, 18, 0, 0)
