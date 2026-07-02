from app.repositories.database import Database


class UsuarioRepository:
    def __init__(self, db: Database):
        self.db = db

    def listar_activos(self) -> list[dict]:
        return self.db.obtener_todos(
            """
            SELECT id_usuario, nombre, correo, rol, estado
            FROM usuarios
            WHERE estado = 'ACTIVO'
            ORDER BY nombre
            """
        )

