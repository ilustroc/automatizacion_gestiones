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
    clave_unica: str | None = None

    def generar_clave_unica(self) -> str:
        fecha = self.fecha_gestion.strftime("%Y-%m-%d %H:%M:%S")
        return f"{self.dni}|{self.telefono}|{fecha}|{self.status}|{self.tipificacion}"
