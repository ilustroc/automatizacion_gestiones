# Modelo de base de datos

La versión final reemplaza el modelo de una sola base por dos servidores:

- `escarperu_software.gestiones`: origen ESCALL, solo lectura mediante SP.
- `automatizacion_gestiones`: destino local con datos procesados, controles, reportes, envíos y logs.

La descripción completa está en `modelo_fisico_base_datos.md`; el diagrama está en `plantuml/modelo_relacional.puml` y los scripts ejecutables están en `docs/sql`.
