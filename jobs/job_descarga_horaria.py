import sys
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from app.config import cargar_configuracion, obtener_configuracion_app
from app.main import main


def calcular_rango_horario(ahora: datetime) -> tuple[datetime, datetime]:
    fecha_hasta = ahora.replace(minute=0, second=0, microsecond=0)
    return fecha_hasta - timedelta(hours=1), fecha_hasta


def ejecutar() -> int:
    cargar_configuracion()
    app_config = obtener_configuracion_app()
    ahora = datetime.now(ZoneInfo(app_config.timezone)).replace(tzinfo=None)
    fecha_desde, fecha_hasta = calcular_rango_horario(ahora)
    return main(
        [
            "--modo",
            "automatico",
            "--fecha-desde",
            fecha_desde.strftime("%Y-%m-%d %H:%M:%S"),
            "--fecha-hasta",
            fecha_hasta.strftime("%Y-%m-%d %H:%M:%S"),
        ]
    )


if __name__ == "__main__":
    raise SystemExit(ejecutar())
