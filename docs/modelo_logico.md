# Modelo logico

El modelo logico se basa en clases simples. Cada clase representa una parte del proceso automatizado.

| Clase | Objeto ejemplo | Atributos principales | Metodos principales |
|---|---|---|---|
| Gestion | `gestion` | fecha_gestion, dni, telefono, status, tipificacion, observacion, fecha_pago, monto_pago, nombre, clave_unica | generar_clave_unica() |
| DescargadorService | `descargador` | gestion_repository | obtener_desde_base_datos(), ejecutar_stored_procedure(), leer_csv() |
| LimpiadorService | `limpiador` | columnas opcionales | limpiar_dataframe(), limpiar_dni(), limpiar_telefono() |
| HomologadorService | `homologador` | mapas de homologacion | homologar_dataframe(), homologar_status(), homologar_tipificacion() |
| ValidadorService | `validador` | campos requeridos, clave de duplicados | validar_columnas(), obtener_registros_validos(), eliminar_duplicados(), agregar_clave_unica() |
| GestionRepository | `gestion_repository` | db | obtener_gestiones_origen(), insertar_gestiones(), existe_clave_unica() |
| ReporteService | `reporte_service` | reporte_repository | obtener_resumen_desde_bd(), formatear_resumen_bd(), exportar_excel() |
| NotificacionService | `notificacion_service` | envio_repository | enviar_reporte(), registrar_intento_envio() |

## Relacion con POO

El proyecto usa clases para agrupar responsabilidades. Los objetos se crean durante la ejecucion y colaboran entre si: los servicios procesan datos y los repositorios acceden a la base de datos.

