from app.repositories.database import DatabaseConnection


class EnvioReporteRepository:
    def __init__(self, target_db: DatabaseConnection):
        self.target_db = target_db

    def registrar_envio(
        self,
        tipo_reporte: str,
        destinatario: str,
        asunto: str,
        estado_envio: str,
        mensaje_error: str | None = None,
    ) -> int:
        return self.target_db.ejecutar_y_obtener_id(
            """
            INSERT INTO envios_reportes (
                tipo_reporte, destinatario, asunto, estado_envio,
                mensaje_error, fecha_envio
            )
            VALUES (
                %s, %s, %s, %s, %s,
                CASE WHEN %s = 'ENVIADO' THEN CURRENT_TIMESTAMP ELSE NULL END
            )
            """,
            (
                tipo_reporte,
                destinatario,
                asunto,
                estado_envio,
                mensaje_error,
                estado_envio,
            ),
        )
