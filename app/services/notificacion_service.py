from pathlib import Path

from app.repositories.envio_reporte_repository import EnvioReporteRepository


class NotificacionService:
    """Servicio preparado para el futuro envio de reportes por correo."""

    def __init__(self, envio_repository: EnvioReporteRepository | None = None):
        self.envio_repository = envio_repository

    def enviar_reporte(self, ruta_reporte: Path, destinatarios: list[str]) -> None:
        # Futuro: aqui se enviara el reporte por SMTP o un servicio externo.
        print(f"Preparado para enviar {ruta_reporte} a {len(destinatarios)} destinatarios.")

    def registrar_intento_envio(
        self,
        id_reporte: int,
        id_destinatario: int,
        estado_envio: str = "PENDIENTE",
        mensaje_error: str | None = None,
    ) -> None:
        if not self.envio_repository:
            raise ValueError("NotificacionService requiere un EnvioReporteRepository.")
        self.envio_repository.registrar_intento(
            id_reporte=id_reporte,
            id_destinatario=id_destinatario,
            estado_envio=estado_envio,
            mensaje_error=mensaje_error,
        )
