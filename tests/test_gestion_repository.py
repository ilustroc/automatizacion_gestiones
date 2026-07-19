from app.repositories.gestion_procesada_repository import GestionProcesadaRepository


class FakeDatabase:
    def __init__(self):
        self.lotes = []

    def ejecutar_lote(self, sql, parametros):
        self.lotes.append((sql, parametros))
        return len(parametros) - (1 if len(self.lotes) == 1 else 0)


def test_insercion_por_lotes_cuenta_insertados_y_duplicados():
    db = FakeDatabase()
    repository = GestionProcesadaRepository(db, batch_size=2)
    gestiones = [
        {
            "id": indice,
            "fecha_gestion": "2026-07-18 08:00:00",
            "dni": f"0000000{indice}",
            "status_homologado": "DIRECTO",
            "tipificacion_homologada": "PROMESA DE PAGO",
            "clave_unica": str(indice) * 64,
        }
        for indice in (1, 2, 3)
    ]
    insertados, duplicados = repository.insertar_lote(gestiones, 9)
    assert len(db.lotes) == 2
    assert insertados == 2
    assert duplicados == 1
    assert all(parametros[-1] == 9 for _, lote in db.lotes for parametros in lote)
