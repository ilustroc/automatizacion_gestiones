import pandas as pd


class ValidadorService:
    CAMPOS_REQUERIDOS = [
        "fecha_gestion",
        "dni",
        "status",
        "tipificacion",
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

    def obtener_registros_validos(self, df: pd.DataFrame) -> tuple[pd.DataFrame, int]:
        self.validar_columnas(df)
        total_antes = len(df)
        mascara_validos = df[self.CAMPOS_REQUERIDOS].notna().all(axis=1)

        for columna in self.CAMPOS_REQUERIDOS:
            mascara_validos = mascara_validos & (df[columna].astype(str).str.strip() != "")

        df_validos = df[mascara_validos].copy()
        descartados = total_antes - len(df_validos)
        return df_validos, descartados

    def eliminar_duplicados(self, df: pd.DataFrame) -> tuple[pd.DataFrame, int]:
        total_antes = len(df)
        df_sin_duplicados = df.drop_duplicates(subset=self.CLAVE_DUPLICADOS).copy()
        duplicados = total_antes - len(df_sin_duplicados)
        return df_sin_duplicados, duplicados

    def agregar_clave_unica(self, df: pd.DataFrame) -> pd.DataFrame:
        df_con_clave = df.copy()
        fechas = df_con_clave["fecha_gestion"].dt.strftime("%Y-%m-%d %H:%M:%S")

        df_con_clave["clave_unica"] = (
            df_con_clave["dni"].astype(str)
            + "|"
            + df_con_clave["telefono"].astype(str)
            + "|"
            + fechas.astype(str)
            + "|"
            + df_con_clave["status"].astype(str)
            + "|"
            + df_con_clave["tipificacion"].astype(str)
        )

        return df_con_clave
