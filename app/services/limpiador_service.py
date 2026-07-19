from decimal import Decimal, InvalidOperation

import pandas as pd

from app.utils.date_utils import convertir_fecha
from app.utils.text_utils import limpiar_espacios, solo_numeros


class LimpiadorService:
    COLUMNAS_OPCIONALES = [
        "telefono",
        "observacion",
        "fecha_pago",
        "monto_pago",
        "nombre",
    ]

    def limpiar_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        df_limpio = df.copy()
        for columna in self.COLUMNAS_OPCIONALES:
            if columna not in df_limpio.columns:
                df_limpio[columna] = None

        if "id_gestion_origen" not in df_limpio.columns and "id" in df_limpio.columns:
            df_limpio["id_gestion_origen"] = df_limpio["id"]

        df_limpio["dni"] = df_limpio["dni"].apply(self.limpiar_dni)
        df_limpio["telefono"] = df_limpio["telefono"].apply(self.limpiar_telefono)
        df_limpio["status"] = df_limpio["status"].apply(limpiar_espacios)
        df_limpio["tipificacion"] = df_limpio["tipificacion"].apply(limpiar_espacios)
        df_limpio["observacion"] = df_limpio["observacion"].apply(
            self.limpiar_texto_opcional
        )
        df_limpio["nombre"] = df_limpio["nombre"].apply(self.limpiar_texto_opcional)
        df_limpio["nombre_asesor"] = df_limpio["nombre"]
        df_limpio["fecha_gestion"] = convertir_fecha(df_limpio["fecha_gestion"])
        df_limpio["fecha_pago"] = convertir_fecha(df_limpio["fecha_pago"])
        df_limpio["monto_pago"] = df_limpio["monto_pago"].apply(
            self.convertir_monto
        )
        return df_limpio

    def limpiar_dni(self, dni: object) -> str:
        return solo_numeros(dni)

    def limpiar_telefono(self, telefono: object) -> str | None:
        numero = solo_numeros(telefono)
        return numero or None

    @staticmethod
    def limpiar_texto_opcional(valor: object) -> str | None:
        if valor is None or (not isinstance(valor, str) and pd.isna(valor)):
            return None
        texto = limpiar_espacios(valor)
        return texto or None

    @staticmethod
    def convertir_monto(valor: object) -> Decimal | None:
        if valor is None or (not isinstance(valor, str) and pd.isna(valor)):
            return None
        texto = str(valor).strip().replace("S/", "").replace(" ", "")
        if not texto:
            return None
        if "," in texto and "." in texto:
            texto = texto.replace(".", "").replace(",", ".")
        elif "," in texto:
            texto = texto.replace(",", ".")
        try:
            return Decimal(texto)
        except InvalidOperation:
            return None
