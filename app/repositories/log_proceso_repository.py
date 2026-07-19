from app.repositories.database import DatabaseConnection


class LogProcesoRepository:
    def __init__(self, target_db: DatabaseConnection):
        self.target_db = target_db

    def registrar(
        self,
        mensaje: str,
        nivel: str = "INFO",
        proceso: str = "GESTIONES",
        id_control_descarga: int | None = None,
        detalle_error: str | None = None,
    ) -> None:
        self.target_db.ejecutar(
            """
            INSERT INTO logs_proceso (
                proceso, nivel, mensaje, id_control_descarga, detalle_error
            )
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                proceso,
                nivel,
                mensaje,
                id_control_descarga,
                detalle_error,
            ),
        )
