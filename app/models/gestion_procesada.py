from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal


@dataclass(slots=True)
class GestionProcesada:
    id_gestion_origen: int
    fecha_gestion: datetime
    dni: str
    telefono: str | None
    status_original: str | None
    tipificacion_original: str | None
    status_homologado: str
    tipificacion_homologada: str
    observacion: str | None
    fecha_pago: date | None
    monto_pago: Decimal | None
    nombre_asesor: str | None
    clave_unica: str
    id_control_descarga: int | None = None
