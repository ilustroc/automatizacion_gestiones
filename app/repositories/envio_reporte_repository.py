from app.repositories.database import Database


class EnvioReporteRepository:
    def __init__(self, db: Database):
        self.db = db

    def registrar_intento(
        self,
        id_reporte: int,
        id_destinatario: int,
        estado_envio: str = "PENDIENTE",
        mensaje_error: str | None = None,
    ) -> None:
        self.db.ejecutar(
            """
            INSERT INTO envios_reportes (
                id_reporte,
                id_destinatario,
                estado_envio,
                mensaje_error
            )
            VALUES (%s, %s, %s, %s)
            """,
            (id_reporte, id_destinatario, estado_envio, mensaje_error),
        )

