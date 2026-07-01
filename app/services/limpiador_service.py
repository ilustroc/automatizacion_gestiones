import pandas as pd

from app.utils.date_utils import convertir_fecha
from app.utils.text_utils import limpiar_espacios, solo_numeros


class LimpiadorService:
    def limpiar_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        df_limpio = df.copy()

        df_limpio["dni"] = df_limpio["dni"].apply(self.limpiar_dni)
        df_limpio["telefono"] = df_limpio["telefono"].apply(self.limpiar_telefono)
        df_limpio["status"] = df_limpio["status"].apply(limpiar_espacios)
        df_limpio["tipificacion"] = df_limpio["tipificacion"].apply(limpiar_espacios)
        df_limpio["observacion"] = df_limpio["observacion"].apply(limpiar_espacios)
        df_limpio["nombre"] = df_limpio["nombre"].apply(limpiar_espacios)
        df_limpio["fecha_gestion"] = convertir_fecha(df_limpio["fecha_gestion"])
        df_limpio["fecha_pago"] = convertir_fecha(df_limpio["fecha_pago"])
        df_limpio["monto_pago"] = pd.to_numeric(df_limpio["monto_pago"], errors="coerce")

        return df_limpio

    def limpiar_dni(self, dni: object) -> str:
        return solo_numeros(dni)

    def limpiar_telefono(self, telefono: object) -> str:
        return solo_numeros(telefono)

