# Requisitos del proyecto

## Requisitos funcionales

1. Conectar a PostgreSQL/Supabase usando variables de entorno.
2. Crear una ejecucion en `cargas_gestiones`.
3. Obtener gestiones desde una consulta SQL o futuro Stored Procedure.
4. Limpiar DNI, telefono, observacion, nombre, fechas y montos.
5. Homologar status y tipificacion.
6. Validar campos obligatorios.
7. Generar `clave_unica`.
8. Eliminar duplicados del lote.
9. Insertar gestiones no duplicadas en `gestiones`.
10. Actualizar la ejecucion con registros descargados, insertados y duplicados.
11. Registrar eventos en `logs_proceso`.
12. Consultar `vw_resumen_gestiones`.
13. Mostrar resumen en consola.

## Requisitos no funcionales

1. Usar Python 3.11 o superior.
2. Mantener codigo simple y entendible.
3. Separar responsabilidades por capas.
4. Evitar patrones avanzados innecesarios.
5. Documentar el proyecto para GitHub y exposicion academica.
6. Proteger credenciales mediante variables de entorno.
7. Ejecutar pruebas unitarias sin depender de Supabase real.

## Alcance actual

La version actual trabaja con PostgreSQL/Supabase como flujo principal. El CSV queda solo como respaldo academico o ejemplo.

## Fuera de alcance en esta etapa

- Interfaz grafica.
- Envio real de correos.
- Automatizacion programada por calendario.
- Stored Procedure real obligatorio.
- Dashboard web.

