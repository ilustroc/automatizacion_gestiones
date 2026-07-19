import pandas as pd
import pytest

from app.services.homologador_service import HomologadorService
from app.services.limpiador_service import LimpiadorService
from app.services.procesador_gestiones_service import ProcesadorGestionesService
from app.services.validador_service import ValidadorService


class FakeTargetDb:
    def __init__(self):
        self.commits = 0
        self.rollbacks = 0

    def commit(self):
        self.commits += 1

    def rollback(self):
        self.rollbacks += 1


class FakeControlRepo:
    def __init__(self):
        self.estado = None
        self.contadores = None

    def marcar_en_proceso(self, control):
        self.estado = "EN_PROCESO"

    def actualizar_contadores(self, control, **contadores):
        self.contadores = contadores

    def marcar_finalizado(self, control):
        self.estado = "FINALIZADO"

    def marcar_error(self, control, mensaje):
        self.estado = "ERROR"


class FakeLogRepo:
    def __init__(self):
        self.logs = []

    def registrar(self, mensaje, **kwargs):
        self.logs.append((mensaje, kwargs))


class FakeGestionRepo:
    def insertar_lote(self, gestiones, control):
        return len(gestiones), 0


class FakeDescargador:
    def descargar_por_rango(self, desde, hasta):
        return pd.DataFrame(
            [
                {
                    "id": 1,
                    "fecha_gestion": "2026-07-18 08:30:00",
                    "dni": "00123456",
                    "telefono": "999-888-777",
                    "status": "CD",
                    "tipificacion": "PDP",
                    "nombre": "Ana",
                }
            ]
        )


def _servicio(descargador):
    db = FakeTargetDb()
    control = FakeControlRepo()
    servicio = ProcesadorGestionesService(
        db,
        control,
        FakeGestionRepo(),
        FakeLogRepo(),
        descargador,
        LimpiadorService(),
        HomologadorService(),
        ValidadorService(),
    )
    return servicio, db, control


def test_procesamiento_de_rango_confirma_transaccion():
    servicio, db, control = _servicio(FakeDescargador())
    resultado = servicio.procesar_control(
        {
            "id_control": 4,
            "fecha_desde": pd.Timestamp("2026-07-18 08:00:00"),
            "fecha_hasta": pd.Timestamp("2026-07-18 09:00:00"),
        }
    )
    assert resultado.registros_insertados == 1
    assert control.estado == "FINALIZADO"
    assert db.commits == 2


def test_error_de_procesamiento_hace_rollback_y_marca_control():
    class DescargadorConError:
        def descargar_por_rango(self, desde, hasta):
            raise RuntimeError("timeout simulado")

    servicio, db, control = _servicio(DescargadorConError())
    with pytest.raises(RuntimeError, match="timeout simulado"):
        servicio.procesar_control(
            {
                "id_control": 4,
                "fecha_desde": pd.Timestamp("2026-07-18 08:00:00"),
                "fecha_hasta": pd.Timestamp("2026-07-18 09:00:00"),
            }
        )
    assert db.rollbacks == 1
    assert control.estado == "ERROR"
