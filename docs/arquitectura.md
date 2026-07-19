# Arquitectura

La arquitectura vigente se documenta en `modelo_logico.md`, `modelo_fisico_base_datos.md` y `plantuml/arquitectura_solucion.puml`.

```text
CLI / Tkinter / jobs
-> servicios de aplicación
-> repositorio origen de solo lectura + repositorios destino
-> ESCALL MySQL                 + MySQL/MariaDB local
-> vistas locales -> reportes -> SMTP
```

La conexión de ESCALL y la conexión local tienen variables, timeouts, permisos y transacciones independientes.
