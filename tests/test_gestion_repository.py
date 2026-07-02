from app.repositories.gestion_repository import GestionRepository


class FakeDatabase:
    def __init__(self):
        self.llamadas = 0

    def insertar_y_retornar(self, sql, parametros):
        self.llamadas += 1
        if self.llamadas == 1:
            return {"id_gestion": 10}
        return None


def test_insertar_gestiones_cuenta_insertados_y_duplicados():
    db = FakeDatabase()
    repository = GestionRepository(db)
    gestiones = [
        {
            "fecha_gestion": "2026-06-01 09:15:00",
            "dni": "12345678",
            "telefono": "987654321",
            "status": "DIRECTO",
            "tipificacion": "PROMESA DE PAGO",
            "clave_unica": "1",
        },
        {
            "fecha_gestion": "2026-06-01 09:15:00",
            "dni": "12345678",
            "telefono": "987654321",
            "status": "DIRECTO",
            "tipificacion": "PROMESA DE PAGO",
            "clave_unica": "1",
        },
    ]

    insertados, duplicados = repository.insertar_gestiones(gestiones, id_carga=1)

    assert insertados == 1
    assert duplicados == 1

