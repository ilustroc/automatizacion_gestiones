from app.repositories.database import DatabaseConnection


class CargaGestionRepository:
    """Historial complementario de cargas guardado en la base local."""

    def __init__(self, target_db: DatabaseConnection):
        self.target_db = target_db

    def crear_carga(
        self,
        id_control_descarga: int | None,
        nombre_fuente: str = "ESCALL_SP",
    ) -> int:
        return self.target_db.ejecutar_y_obtener_id(
            """
            INSERT INTO cargas_gestiones (
                id_control_descarga, nombre_fuente, estado
            )
            VALUES (%s, %s, 'INICIADO')
            """,
            (id_control_descarga, nombre_fuente),
        )

    def finalizar_carga(
        self,
        id_carga: int,
        registros_descargados: int,
        registros_insertados: int,
        registros_duplicados: int,
        registros_invalidos: int = 0,
        estado: str = "FINALIZADO",
        mensaje_error: str | None = None,
    ) -> None:
        self.target_db.ejecutar(
            """
            UPDATE cargas_gestiones
            SET estado = %s, registros_descargados = %s,
                registros_insertados = %s, registros_duplicados = %s,
                registros_invalidos = %s, mensaje_error = %s
            WHERE id_carga = %s
            """,
            (
                estado,
                registros_descargados,
                registros_insertados,
                registros_duplicados,
                registros_invalidos,
                mensaje_error,
                id_carga,
            ),
        )
