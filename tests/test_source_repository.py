from datetime import datetime

from app.repositories.source_gestion_repository import SourceGestionRepository


class FakeSourceDatabase:
    def __init__(self):
        self.procedimientos = []
        self.consultas = []

    def ejecutar_procedimiento(self, nombre, parametros):
        self.procedimientos.append((nombre, parametros))
        return [{"id": 1}]

    def obtener_uno(self, sql, parametros):
        self.consultas.append((sql, parametros))
        return {"total": 1}


def test_source_repository_usa_sp_parametrizado_y_solo_lectura():
    db = FakeSourceDatabase()
    repo = SourceGestionRepository(db)
    desde = datetime(2026, 7, 18, 8)
    hasta = datetime(2026, 7, 18, 9)
    assert repo.obtener_gestiones_por_rango(desde, hasta) == [{"id": 1}]
    assert db.procedimientos == [("sp_descargar_gestiones_rango", (desde, hasta))]
    assert not hasattr(repo, "insertar")


def test_source_repository_divide_resultados_en_lotes():
    db = FakeSourceDatabase()
    db.ejecutar_procedimiento = lambda *args: [{"id": i} for i in range(5)]
    repo = SourceGestionRepository(db)
    lotes = list(
        repo.obtener_gestiones_por_lotes(
            datetime(2026, 7, 18, 8), datetime(2026, 7, 18, 9), 2
        )
    )
    assert [len(lote) for lote in lotes] == [2, 2, 1]
