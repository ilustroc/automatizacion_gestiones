import smtplib
from email.message import EmailMessage
from pathlib import Path

from app.config import SmtpConfig
from app.exceptions import NotificacionError
from app.repositories.envio_reporte_repository import EnvioReporteRepository


class NotificacionService:
    def __init__(
        self,
        envio_repository: EnvioReporteRepository,
        smtp_config: SmtpConfig | None = None,
        *,
        simulacion: bool = False,
    ):
        self.envio_repository = envio_repository
        self.smtp_config = smtp_config
        self.simulacion = simulacion

    def probar_conexion_smtp(self) -> bool:
        if self.smtp_config is None:
            raise NotificacionError("La configuracion SMTP no esta disponible.")
        try:
            with self._abrir_smtp() as smtp:
                smtp.login(self.smtp_config.user, self.smtp_config.password)
            return True
        except (OSError, smtplib.SMTPException) as error:
            raise NotificacionError(
                "No se pudo autenticar con el servidor SMTP."
            ) from error

    def enviar_html(
        self,
        tipo_reporte: str,
        destinatario: str,
        asunto: str,
        html: str,
        adjunto: Path | None = None,
    ) -> bool:
        if adjunto is not None:
            return self.enviar_con_adjunto(
                tipo_reporte, destinatario, asunto, html, adjunto
            )
        return self._enviar(tipo_reporte, destinatario, asunto, html, None)

    def enviar_con_adjunto(
        self,
        tipo_reporte: str,
        destinatario: str,
        asunto: str,
        html: str,
        adjunto: Path,
    ) -> bool:
        return self._enviar(tipo_reporte, destinatario, asunto, html, adjunto)

    def _enviar(
        self,
        tipo_reporte: str,
        destinatario: str,
        asunto: str,
        html: str,
        adjunto: Path | None,
    ) -> bool:
        if not destinatario:
            return self._registrar_error(
                tipo_reporte, destinatario, asunto, "Destinatario no configurado"
            )
        if self.simulacion:
            self.envio_repository.registrar_envio(
                tipo_reporte,
                destinatario,
                asunto,
                "PENDIENTE",
                "Modo simulacion: correo no enviado.",
            )
            return True
        if self.smtp_config is None:
            return self._registrar_error(
                tipo_reporte,
                destinatario,
                asunto,
                "Configuracion SMTP no disponible",
            )

        try:
            mensaje = self._crear_mensaje(destinatario, asunto, html, adjunto)
            with self._abrir_smtp() as smtp:
                smtp.login(self.smtp_config.user, self.smtp_config.password)
                smtp.send_message(mensaje)
            self.envio_repository.registrar_envio(
                tipo_reporte, destinatario, asunto, "ENVIADO"
            )
            return True
        except (OSError, smtplib.SMTPException, FileNotFoundError) as error:
            return self._registrar_error(
                tipo_reporte,
                destinatario,
                asunto,
                f"{error.__class__.__name__}: {error}",
            )

    def _abrir_smtp(self):
        if self.smtp_config is None:
            raise NotificacionError("La configuracion SMTP no esta disponible.")
        if self.smtp_config.use_ssl:
            return smtplib.SMTP_SSL(
                self.smtp_config.host, self.smtp_config.port, timeout=30
            )
        smtp = smtplib.SMTP(self.smtp_config.host, self.smtp_config.port, timeout=30)
        smtp.starttls()
        return smtp

    def _crear_mensaje(
        self,
        destinatario: str,
        asunto: str,
        html: str,
        adjunto: Path | None,
    ) -> EmailMessage:
        if self.smtp_config is None:
            raise NotificacionError("La configuracion SMTP no esta disponible.")
        mensaje = EmailMessage()
        mensaje["Subject"] = asunto
        mensaje["From"] = (
            f"{self.smtp_config.from_name} <{self.smtp_config.from_email}>"
        )
        mensaje["To"] = destinatario
        mensaje.set_content("Este correo contiene un reporte automatico de gestiones.")
        mensaje.add_alternative(html, subtype="html")
        if adjunto is not None:
            contenido = adjunto.read_bytes()
            mensaje.add_attachment(
                contenido,
                maintype="application",
                subtype="vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                filename=adjunto.name,
            )
        return mensaje

    def _registrar_error(
        self,
        tipo_reporte: str,
        destinatario: str,
        asunto: str,
        mensaje: str,
    ) -> bool:
        self.envio_repository.registrar_envio(
            tipo_reporte, destinatario, asunto, "ERROR", mensaje[:2000]
        )
        return False
