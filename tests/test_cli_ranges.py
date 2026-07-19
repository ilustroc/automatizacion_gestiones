import argparse
from datetime import datetime

from app.main import resolver_rango


def test_rango_por_fechas_convierte_fin_a_limite_exclusivo():
    args = argparse.Namespace(
        fecha_inicio="2026-07-01",
        fecha_fin="2026-07-18",
        fecha_desde=None,
        fecha_hasta=None,
    )
    desde, hasta = resolver_rango(args)
    assert desde == datetime(2026, 7, 1)
    assert hasta == datetime(2026, 7, 19)


def test_rango_horario_se_conserva_exactamente():
    args = argparse.Namespace(
        fecha_inicio=None,
        fecha_fin=None,
        fecha_desde="2026-07-18 08:00:00",
        fecha_hasta="2026-07-18 09:00:00",
    )
    assert resolver_rango(args) == (
        datetime(2026, 7, 18, 8),
        datetime(2026, 7, 18, 9),
    )
