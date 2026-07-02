from pathlib import Path

import pandas as pd

from app.repositories.gestion_repository import GestionRepository


class DescargadorService:
    """Obtiene gestiones desde PostgreSQL/Supabase."""

    def __init__(self, gestion_repository: GestionRepository | None = None):
        self.gestion_repository = gestion_repository

    def obtener_desde_base_datos(self, consulta_sql: str | None = None) -> pd.DataFrame:
        if not self.gestion_repository:
            raise ValueError("DescargadorService requiere un GestionRepository.")
        registros = self.gestion_repository.obtener_gestiones_origen(consulta_sql)
        return pd.DataFrame(registros)

    def leer_csv(self, ruta_entrada: Path) -> pd.DataFrame:
        """Lectura de respaldo para ejemplos academicos, no es el flujo principal."""
        return pd.read_csv(ruta_entrada, dtype=str, encoding="utf-8")

    def ejecutar_stored_procedure(self, nombre_sp: str) -> pd.DataFrame:
        consulta = f"SELECT * FROM {nombre_sp}()"
        return self.obtener_desde_base_datos(consulta)

