# Modelo base de datos

La base futura sera relacional y puede implementarse en PostgreSQL usando Supabase.

## Tablas sugeridas

### empresas

Guarda informacion de las empresas o carteras gestionadas.

### gestiones

Guarda cada gestion limpia con sus datos operativos principales.

### tipificaciones

Catalogo de tipificaciones homologadas.

### ejecuciones

Registra cada ejecucion del proceso, cantidad de registros leidos, duplicados y archivo generado.

### reportes_generados

Registra los reportes creados y su estado de envio.

## Relacion general

- Una empresa tiene muchas gestiones.
- Una tipificacion puede estar asociada a muchas gestiones.
- Una ejecucion puede generar uno o mas reportes.

