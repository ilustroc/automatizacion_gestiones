from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal


@dataclass(slots=True)
class GestionOrigen:
    id: int
    fecha_gestion: datetime
    dni: str
    telefono: str | None
    status: str
    tipificacion: str
    observacion: str | None = None
    fecha_pago: date | None = None
    monto_pago: Decimal | None = None
    nombre: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
