import re

from app.repositories.database import DatabaseConnection


class SourceSchemaRepository:
    COLUMNAS_MINIMAS_GESTIONES = {
        "id",
        "fecha_gestion",
        "dni",
        "telefono",
        "status",
        "tipificacion",
        "observacion",
        "fecha_pago",
        "monto_pago",
        "nombre",
        "created_at",
        "updated_at",
    }

    def __init__(self, source_db: DatabaseConnection):
        self.source_db = source_db

    def tabla_existe(self, nombre_tabla: str) -> bool:
        fila = self.source_db.obtener_uno(
            """
            SELECT COUNT(*) AS total
            FROM information_schema.tables
            WHERE table_schema = %s AND table_name = %s
            """,
            (self.source_db.config.name, nombre_tabla),
        )
        return bool(fila and fila["total"] > 0)

    def obtener_columnas(self, nombre_tabla: str) -> list[dict]:
        self._validar_identificador(nombre_tabla)
        return self.source_db.ejecutar_consulta(f"SHOW COLUMNS FROM `{nombre_tabla}`")

    def procedimiento_existe(self, nombre_procedimiento: str) -> bool:
        fila = self.source_db.obtener_uno(
            """
            SELECT COUNT(*) AS total
            FROM information_schema.routines
            WHERE routine_schema = %s
              AND routine_name = %s
              AND routine_type = 'PROCEDURE'
            """,
            (self.source_db.config.name, nombre_procedimiento),
        )
        return bool(fila and fila["total"] > 0)

    def probar_acceso_gestiones(self) -> bool:
        self.source_db.ejecutar_consulta("SELECT 1 AS acceso FROM gestiones LIMIT 1")
        return True

    def obtener_version_mysql(self) -> str:
        fila = self.source_db.obtener_uno("SELECT VERSION() AS version")
        return str(fila["version"]) if fila else "desconocida"

    def columnas_faltantes_gestiones(self) -> list[str]:
        columnas = {
            str(columna.get("Field", columna.get("COLUMN_NAME", ""))).lower()
            for columna in self.obtener_columnas("gestiones")
        }
        return sorted(self.COLUMNAS_MINIMAS_GESTIONES - columnas)

    @staticmethod
    def _validar_identificador(nombre: str) -> None:
        if not re.fullmatch(r"[A-Za-z0-9_]+", nombre):
            raise ValueError("El nombre de tabla contiene caracteres no permitidos.")
