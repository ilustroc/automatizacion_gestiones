import pandas as pd


class GestionRepository:
    """Repositorio base para una futura carga en PostgreSQL/Supabase."""

    def guardar_gestiones(self, df: pd.DataFrame) -> None:
        # En una version futura aqui se insertaran las gestiones en la base de datos.
        print(f"Preparado para guardar {len(df)} gestiones en base de datos.")

