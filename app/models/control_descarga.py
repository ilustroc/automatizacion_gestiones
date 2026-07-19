from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class ControlDescarga:
    fecha_desde: datetime
    fecha_hasta: datetime
    tipo_descarga: str
    descripcion: str | None = None
    id_control: int | None = None
    estado: str = "PENDIENTE"
    registros_origen: int = 0
    registros_insertados: int = 0
    registros_duplicados: int = 0
    registros_invalidos: int = 0
