import pandas as pd


class ValidadorService:
    CAMPOS_REQUERIDOS = [
        "fecha_gestion",
        "dni",
        "telefono",
        "status",
        "tipificacion",
        "observacion",
        "fecha_pago",
        "monto_pago",
        "nombre",
    ]

    CLAVE_DUPLICADOS = [
        "dni",
        "telefono",
        "fecha_gestion",
        "status",
        "tipificacion",
    ]

    def validar_columnas(self, df: pd.DataFrame) -> None:
        columnas_faltantes = [
            columna for columna in self.CAMPOS_REQUERIDOS if columna not in df.columns
        ]
        if columnas_faltantes:
            faltantes = ", ".join(columnas_faltantes)
            raise ValueError(f"Faltan columnas requeridas: {faltantes}")

    def eliminar_duplicados(self, df: pd.DataFrame) -> tuple[pd.DataFrame, int]:
        total_antes = len(df)
        df_sin_duplicados = df.drop_duplicates(subset=self.CLAVE_DUPLICADOS).copy()
        duplicados = total_antes - len(df_sin_duplicados)
        return df_sin_duplicados, duplicados

