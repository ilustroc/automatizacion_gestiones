from app.repositories.database import Database


class CarteraRepository:
    def __init__(self, db: Database):
        self.db = db

    def listar_activas(self) -> list[dict]:
        return self.db.obtener_todos(
            """
            SELECT id_cartera, id_empresa, nombre_cartera, descripcion, estado
            FROM carteras
            WHERE estado = 'ACTIVO'
            ORDER BY nombre_cartera
            """
        )

