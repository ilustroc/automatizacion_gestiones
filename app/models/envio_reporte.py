from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class EnvioReporte:
    tipo_reporte: str
    destinatario: str
    asunto: str
    estado_envio: str = "PENDIENTE"
    mensaje_error: str | None = None
    fecha_envio: datetime | None = None
    id_envio: int | None = None
