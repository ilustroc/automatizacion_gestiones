from datetime import datetime, timedelta

from app.repositories.database import DatabaseConnection


class ControlDescargaRepository:
    def __init__(self, target_db: DatabaseConnection):
        self.target_db = target_db

    def crear_control(
        self,
        fecha_desde: datetime,
        fecha_hasta: datetime,
        tipo_descarga: str = "MANUAL",
        descripcion: str | None = None,
    ) -> int:
        self._validar_rango(fecha_desde, fecha_hasta)
        tipo = tipo_descarga.upper()
        if tipo not in {"MANUAL", "AUTOMATICA"}:
            raise ValueError("tipo_descarga debe ser MANUAL o AUTOMATICA.")
        return self.target_db.ejecutar_y_obtener_id(
            """
            INSERT INTO control_descargas_gestiones (
                fecha_desde, fecha_hasta, estado, tipo_descarga, descripcion
            )
            VALUES (%s, %s, 'PENDIENTE', %s, %s)
            """,
            (fecha_desde, fecha_hasta, tipo, descripcion),
        )

    def obtener_pendiente(self) -> dict | None:
        return self.target_db.obtener_uno(
            """
            SELECT * FROM vw_control_descargas_pendientes
            ORDER BY fecha_desde, id_control
            LIMIT 1
            """
        )

    def obtener_por_id(self, id_control: int) -> dict | None:
        return self.target_db.obtener_uno(
            "SELECT * FROM control_descargas_gestiones WHERE id_control = %s",
            (id_control,),
        )

    def marcar_en_proceso(self, id_control: int) -> None:
        self.target_db.ejecutar(
            """
            UPDATE control_descargas_gestiones
            SET estado = 'EN_PROCESO', fecha_inicio_proceso = CURRENT_TIMESTAMP,
                fecha_fin_proceso = NULL, mensaje_error = NULL
            WHERE id_control = %s
            """,
            (id_control,),
        )

    def actualizar_contadores(
        self,
        id_control: int,
        *,
        registros_origen: int,
        registros_insertados: int,
        registros_duplicados: int,
        registros_invalidos: int,
    ) -> None:
        self.target_db.ejecutar(
            """
            UPDATE control_descargas_gestiones
            SET registros_origen = %s, registros_insertados = %s,
                registros_duplicados = %s, registros_invalidos = %s
            WHERE id_control = %s
            """,
            (
                registros_origen,
                registros_insertados,
                registros_duplicados,
                registros_invalidos,
                id_control,
            ),
        )

    def marcar_finalizado(self, id_control: int) -> None:
        self.target_db.ejecutar(
            """
            UPDATE control_descargas_gestiones
            SET estado = 'FINALIZADO', fecha_fin_proceso = CURRENT_TIMESTAMP,
                mensaje_error = NULL
            WHERE id_control = %s
            """,
            (id_control,),
        )

    def marcar_error(self, id_control: int, mensaje: str) -> None:
        self.target_db.ejecutar(
            """
            UPDATE control_descargas_gestiones
            SET estado = 'ERROR', mensaje_error = %s,
                fecha_fin_proceso = CURRENT_TIMESTAMP
            WHERE id_control = %s
            """,
            (mensaje[:2000], id_control),
        )

    def listar_ultimos(self, limite: int = 20) -> list[dict]:
        limite_seguro = max(1, min(int(limite), 100))
        return self.target_db.ejecutar_consulta(
            f"""
            SELECT id_control, fecha_desde, fecha_hasta, estado, tipo_descarga,
                   registros_origen, registros_insertados, registros_duplicados,
                   registros_invalidos, descripcion, created_at
            FROM control_descargas_gestiones
            ORDER BY id_control DESC
            LIMIT {limite_seguro}
            """
        )

    @staticmethod
    def calcular_ultima_hora(ahora: datetime) -> tuple[datetime, datetime]:
        fecha_hasta = ahora.replace(minute=0, second=0, microsecond=0)
        return fecha_hasta - timedelta(hours=1), fecha_hasta

    @staticmethod
    def _validar_rango(fecha_desde: datetime, fecha_hasta: datetime) -> None:
        if fecha_hasta <= fecha_desde:
            raise ValueError("fecha_hasta debe ser mayor que fecha_desde.")

    # Alias de compatibilidad con la version previa.
    finalizar = marcar_finalizado
