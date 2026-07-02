from datetime import date

from app.repositories.database import Database


class CargaGestionRepository:
    def __init__(self, db: Database):
        self.db = db

    def crear_carga(
        self,
        periodo_desde: date,
        periodo_hasta: date,
        origen: str = "BASE_DATOS",
        nombre_sp: str | None = None,
    ) -> int:
        fila = self.db.insertar_y_retornar(
            """
            INSERT INTO cargas_gestiones (
                periodo_desde,
                periodo_hasta,
                origen,
                nombre_sp,
                estado
            )
            VALUES (%s, %s, %s, %s, 'INICIADO')
            RETURNING id_carga
            """,
            (periodo_desde, periodo_hasta, origen, nombre_sp),
        )
        return int(fila["id_carga"])

    def finalizar_carga(
        self,
        id_carga: int,
        registros_descargados: int,
        registros_insertados: int,
        registros_duplicados: int,
        estado: str = "FINALIZADO",
        observacion: str | None = None,
    ) -> None:
        self.db.ejecutar(
            """
            UPDATE cargas_gestiones
            SET fecha_fin = NOW(),
                registros_descargados = %s,
                registros_insertados = %s,
                registros_duplicados = %s,
                estado = %s,
                observacion = %s
            WHERE id_carga = %s
            """,
            (
                registros_descargados,
                registros_insertados,
                registros_duplicados,
                estado,
                observacion,
                id_carga,
            ),
        )

