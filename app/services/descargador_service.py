from datetime import datetime

import pandas as pd

from app.repositories.source_gestion_repository import SourceGestionRepository


class DescargadorService:
    """Descarga gestiones de ESCALL mediante un Stored Procedure de solo lectura."""

    def __init__(self, source_repository: SourceGestionRepository):
        self.source_repository = source_repository

    def descargar_por_rango(
        self,
        fecha_desde: datetime,
        fecha_hasta: datetime,
    ) -> pd.DataFrame:
        registros = self.source_repository.obtener_gestiones_por_rango(
            fecha_desde,
            fecha_hasta,
        )
        return pd.DataFrame(registros)
