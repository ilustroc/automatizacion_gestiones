import logging
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_INPUT_DIR = BASE_DIR / "data" / "input"
DATA_OUTPUT_DIR = BASE_DIR / "data" / "output"
LOGS_DIR = BASE_DIR / "logs"

INPUT_FILE = DATA_INPUT_DIR / "gestiones.csv"
OUTPUT_FILE = DATA_OUTPUT_DIR / "gestiones_limpias.xlsx"
LOG_FILE = LOGS_DIR / "proceso.log"


def cargar_configuracion() -> None:
    """Carga variables de entorno y asegura carpetas necesarias."""
    load_dotenv(BASE_DIR / ".env")
    DATA_INPUT_DIR.mkdir(parents=True, exist_ok=True)
    DATA_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    LOGS_DIR.mkdir(parents=True, exist_ok=True)


def configurar_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(LOG_FILE, encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )

