import smtplib

from app.config import SmtpConfig
from app.services.notificacion_service import NotificacionService


class FakeEnvioRepository:
    def __init__(self):
        self.registros = []

    def registrar_envio(self, tipo, destinatario, asunto, estado, error=None):
        self.registros.append((tipo, destinatario, asunto, estado, error))
        return len(self.registros)


class FakeSMTP:
    def __init__(self, *args, **kwargs):
        self.autenticado = False
        self.enviado = False

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def login(self, user, password):
        self.autenticado = True

    def send_message(self, message):
        self.enviado = True


def _smtp_config(use_ssl=True):
    return SmtpConfig(
        host="smtp.example.com",
        port=465 if use_ssl else 587,
        use_ssl=use_ssl,
        user="notificaciones@example.com",
        password="&Clave#{2026}?",
        from_email="notificaciones@example.com",
        from_name="Automatizacion",
    )


def test_smtp_ssl_simulado_registra_envio_exitoso(monkeypatch):
    repo = FakeEnvioRepository()
    monkeypatch.setattr(smtplib, "SMTP_SSL", FakeSMTP)
    servicio = NotificacionService(repo, _smtp_config())
    assert servicio.enviar_html("PROMESAS", "supervisor@example.com", "Asunto", "<p>OK</p>")
    assert repo.registros[-1][3] == "ENVIADO"


def test_error_smtp_simulado_se_registra(monkeypatch):
    class SMTPConError(FakeSMTP):
        def login(self, user, password):
            raise smtplib.SMTPAuthenticationError(535, b"Credenciales invalidas")

    repo = FakeEnvioRepository()
    monkeypatch.setattr(smtplib, "SMTP_SSL", SMTPConError)
    servicio = NotificacionService(repo, _smtp_config())
    assert not servicio.enviar_html("IMPULSE", "empresa@example.com", "Asunto", "<p>OK</p>")
    assert repo.registros[-1][3] == "ERROR"


def test_modo_simulacion_no_abre_smtp_y_registra_pendiente():
    repo = FakeEnvioRepository()
    servicio = NotificacionService(repo, _smtp_config(), simulacion=True)
    assert servicio.enviar_html("GERENCIA", "gerencia@example.com", "Asunto", "<p>OK</p>")
    assert repo.registros[-1][3] == "PENDIENTE"


def test_smtp_starttls_se_usa_cuando_ssl_es_false(monkeypatch):
    instancias = []

    class FakeStartTls(FakeSMTP):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.tls = False
            instancias.append(self)

        def starttls(self):
            self.tls = True

    repo = FakeEnvioRepository()
    monkeypatch.setattr(smtplib, "SMTP", FakeStartTls)
    servicio = NotificacionService(repo, _smtp_config(use_ssl=False))
    assert servicio.enviar_html("IMPULSE", "empresa@example.com", "Asunto", "<p>OK</p>")
    assert instancias[0].tls is True
