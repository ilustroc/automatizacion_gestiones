from app.repositories.database import Database


class EmpresaRepository:
    def __init__(self, db: Database):
        self.db = db

    def listar_activas(self) -> list[dict]:
        return self.db.obtener_todos(
            """
            SELECT id_empresa, nombre_empresa, ruc, estado
            FROM empresas
            WHERE estado = 'ACTIVO'
            ORDER BY nombre_empresa
            """
        )

