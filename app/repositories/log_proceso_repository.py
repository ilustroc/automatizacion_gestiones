from app.repositories.database import Database


class LogProcesoRepository:
    def __init__(self, db: Database):
        self.db = db

    def registrar(self, mensaje: str, nivel: str = "INFO", id_carga: int | None = None) -> None:
        self.db.ejecutar(
            """
            INSERT INTO logs_proceso (id_carga, nivel, mensaje)
            VALUES (%s, %s, %s)
            """,
            (id_carga, nivel, mensaje),
        )

