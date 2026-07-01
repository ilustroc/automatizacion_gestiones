import pandas as pd


def convertir_fecha(serie: pd.Series) -> pd.Series:
    return pd.to_datetime(serie, errors="coerce", dayfirst=True)

