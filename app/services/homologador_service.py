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
        "NO CONTESTA": "NO CONTACTO",
        "NO CONTESTO": "NO CONTACTO",
        "ILOCALIZADO": "NO CONTACTO",
        "INUBICABLE": "NO CONTACTO",
        "SIN GESTION": "SIN GESTIÓN",
        "": "SIN GESTIÓN",
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
        "YA PAGO": "YA PAGÓ",
        "PAGO REALIZADO": "YA PAGÓ",
        "NUMERO INCORRECTO": "NÚMERO INCORRECTO",
        "SIN GESTION": "SIN GESTIÓN",
        "": "SIN GESTIÓN",
    }

    def __init__(self, reglas_tipificacion: dict[str, str] | None = None):
        self.mapa_tipificacion = dict(self.MAPA_TIPIFICACION)
        if reglas_tipificacion:
            self.mapa_tipificacion.update(
                {
                    normalizar_texto(origen): destino
                    for origen, destino in reglas_tipificacion.items()
                }
            )

    def homologar_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        df_homologado = df.copy()
        if "status_original" not in df_homologado.columns:
            df_homologado["status_original"] = df_homologado["status"]
        if "tipificacion_original" not in df_homologado.columns:
            df_homologado["tipificacion_original"] = df_homologado["tipificacion"]

        df_homologado["status_homologado"] = df_homologado["status"].apply(
            self.homologar_status
        )
        df_homologado["tipificacion_homologada"] = df_homologado[
            "tipificacion"
        ].apply(self.homologar_tipificacion)
        return df_homologado

    def homologar_status(self, status: object) -> str:
        texto = normalizar_texto(status)
        return self.MAPA_STATUS.get(texto, "SIN GESTIÓN")

    def homologar_tipificacion(self, tipificacion: object) -> str:
        texto = normalizar_texto(tipificacion)
        return self.mapa_tipificacion.get(texto, texto or "SIN GESTIÓN")
