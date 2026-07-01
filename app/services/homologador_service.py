import pandas as pd

from app.utils.text_utils import normalizar_texto


class HomologadorService:
    MAPA_STATUS = {
        "DIRECTO": "DIRECTO",
        "CONTACTO DIRECTO": "DIRECTO",
        "CD": "DIRECTO",
        "INDIRECTO": "INDIRECTO",
        "CONTACTO INDIRECTO": "INDIRECTO",
        "CI": "INDIRECTO",
        "NO CONTACTO": "NO CONTACTO",
        "NC": "NO CONTACTO",
        "ILOCALIZADO": "NO CONTACTO",
    }

    MAPA_TIPIFICACION = {
        "PDP": "PROMESA DE PAGO",
        "PROMESA": "PROMESA DE PAGO",
        "PROMESA DE PAGO": "PROMESA DE PAGO",
        "NO CONTESTA": "NO CONTESTA",
        "NO CONTESTO": "NO CONTESTA",
        "MENSAJE": "MENSAJE",
        "MSJ": "MENSAJE",
        "ILOCALIZADO": "ILOCALIZADO",
        "YA PAGO": "YA PAGO",
        "PAGO REALIZADO": "YA PAGO",
        "NUMERO INCORRECTO": "NÚMERO INCORRECTO",
    }

    def homologar_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        df_homologado = df.copy()
        df_homologado["status"] = df_homologado["status"].apply(self.homologar_status)
        df_homologado["tipificacion"] = df_homologado["tipificacion"].apply(
            self.homologar_tipificacion
        )
        return df_homologado

    def homologar_status(self, status: object) -> str:
        texto = normalizar_texto(status)
        return self.MAPA_STATUS.get(texto, texto)

    def homologar_tipificacion(self, tipificacion: object) -> str:
        texto = normalizar_texto(tipificacion)
        return self.MAPA_TIPIFICACION.get(texto, texto)

