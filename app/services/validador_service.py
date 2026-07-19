import hashlib

import pandas as pd

from app.exceptions import ValidacionGestionError


class ValidadorService:
    CAMPOS_REQUERIDOS = [
        "id_gestion_origen",
        "fecha_gestion",
        "dni",
        "status_homologado",
        "tipificacion_homologada",
    ]

    def validar_columnas(self, df: pd.DataFrame) -> None:
        faltantes = [columna for columna in self.CAMPOS_REQUERIDOS if columna not in df]
        if faltantes:
            raise ValidacionGestionError(
                "Faltan columnas requeridas: " + ", ".join(faltantes)
            )

    def obtener_registros_validos(self, df: pd.DataFrame) -> tuple[pd.DataFrame, int]:
        self.validar_columnas(df)
        mascara = df[self.CAMPOS_REQUERIDOS].notna().all(axis=1)
        for columna in self.CAMPOS_REQUERIDOS:
            mascara &= df[columna].astype(str).str.strip().ne("")
        mascara &= pd.to_numeric(df["id_gestion_origen"], errors="coerce").gt(0)
        validos = df[mascara].copy()
        return validos, len(df) - len(validos)

    def agregar_clave_unica(self, df: pd.DataFrame) -> pd.DataFrame:
        resultado = df.copy()
        resultado["clave_unica"] = resultado.apply(
            lambda fila: self.generar_clave_unica(
                dni=fila["dni"],
                telefono=fila.get("telefono"),
                fecha_gestion=fila["fecha_gestion"],
                status_homologado=fila["status_homologado"],
                tipificacion_homologada=fila["tipificacion_homologada"],
            ),
            axis=1,
        )
        return resultado

    def eliminar_duplicados(self, df: pd.DataFrame) -> tuple[pd.DataFrame, int]:
        if "clave_unica" not in df.columns:
            df = self.agregar_clave_unica(df)
        resultado = df.drop_duplicates(subset=["clave_unica"]).copy()
        return resultado, len(df) - len(resultado)

    @staticmethod
    def generar_clave_unica(
        dni: object,
        telefono: object,
        fecha_gestion: object,
        status_homologado: object,
        tipificacion_homologada: object,
    ) -> str:
        fecha = pd.Timestamp(fecha_gestion).strftime("%Y-%m-%d %H:%M:%S")
        telefono_limpio = "" if telefono is None or pd.isna(telefono) else str(telefono)
        base = (
            f"{dni}|{telefono_limpio}|{fecha}|"
            f"{status_homologado}|{tipificacion_homologada}"
        )
        return hashlib.sha256(base.encode("utf-8")).hexdigest()
