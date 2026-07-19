from app.exceptions import ValidacionGestionError
from app.repositories.database import DatabaseConnection
from app.repositories.source_schema_repository import SourceSchemaRepository


class DiagnosticoService:
    TABLAS_DESTINO = {
        "empresas",
        "usuarios",
        "carteras",
        "control_descargas_gestiones",
        "cargas_gestiones",
        "gestiones_procesadas",
        "reportes",
        "destinatarios_reportes",
        "envios_reportes",
        "logs_proceso",
    }

    def __init__(
        self,
        source_db: DatabaseConnection | None = None,
        target_db: DatabaseConnection | None = None,
    ):
        self.source_db = source_db
        self.target_db = target_db

    def diagnosticar_origen(self) -> dict:
        if self.source_db is None:
            raise ValueError("La conexion origen no esta disponible.")
        schema = SourceSchemaRepository(self.source_db)
        if not schema.tabla_existe("gestiones"):
            raise ValidacionGestionError(
                "La tabla gestiones no existe en la base origen ESCALL."
            )
        columnas = schema.obtener_columnas("gestiones")
        nombres = [str(fila.get("Field", "")) for fila in columnas]
        faltantes = schema.columnas_faltantes_gestiones()
        if faltantes:
            raise ValidacionGestionError(
                "La tabla gestiones no contiene estas columnas requeridas: "
                + ", ".join(faltantes)
            )
        if not schema.procedimiento_existe("sp_descargar_gestiones_rango"):
            raise ValidacionGestionError(
                "No existe el Stored Procedure sp_descargar_gestiones_rango en ESCALL."
            )
        schema.probar_acceso_gestiones()
        return {
            "version": schema.obtener_version_mysql(),
            "tabla_gestiones": True,
            "columnas": nombres,
            "stored_procedure": True,
        }

    def diagnosticar_destino(self) -> dict:
        if self.target_db is None:
            raise ValueError("La conexion destino no esta disponible.")
        version = self.target_db.obtener_uno("SELECT VERSION() AS version")
        filas = self.target_db.ejecutar_consulta(
            """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = %s
            """,
            (self.target_db.config.name,),
        )
        existentes = {
            str(fila.get("TABLE_NAME", fila.get("table_name", ""))).lower()
            for fila in filas
        }
        faltantes = sorted(self.TABLAS_DESTINO - existentes)
        if faltantes:
            raise ValidacionGestionError(
                "Faltan tablas en la base destino local: " + ", ".join(faltantes)
            )
        return {
            "version": str(version["version"]) if version else "desconocida",
            "tablas": sorted(existentes & self.TABLAS_DESTINO),
        }
