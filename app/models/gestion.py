from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass
class Gestion:
    fecha_gestion: datetime
    dni: str
    telefono: str
    status: str
    tipificacion: str
    observacion: str
    fecha_pago: datetime | None
    monto_pago: Decimal | None
    nombre: str

