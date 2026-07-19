from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path


@dataclass(slots=True)
class Reporte:
    tipo: str
    asunto: str
    html: str
    fecha_desde: datetime | None = None
    fecha_hasta: datetime | None = None
    datos: list[dict] = field(default_factory=list)
    archivo_excel: Path | None = None
