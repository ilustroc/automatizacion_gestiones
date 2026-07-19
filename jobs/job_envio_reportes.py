import argparse
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from app.main import main


def ejecutar(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Job de envio de reportes.")
    parser.add_argument(
        "--reporte",
        choices=["promesas", "impulse", "gerencia", "todos"],
        default="todos",
    )
    parser.add_argument("--solo-generar", action="store_true")
    args = parser.parse_args(argv)
    parametros = ["--reporte", args.reporte]
    parametros.append("--solo-generar" if args.solo_generar else "--enviar")
    return main(parametros)


if __name__ == "__main__":
    raise SystemExit(ejecutar())
