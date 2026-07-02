# Guia de exposicion

Duracion sugerida: 5 a 7 minutos.

## 1. Paradigma de programacion

Explicar que el proyecto usa programacion orientada a objetos. Mencionar que se usan clases, objetos, atributos y metodos para representar el proceso.

Idea clave:

```text
Cada clase tiene una responsabilidad clara dentro de la automatizacion.
```

## 2. Contexto empresarial y problematica

Presentar a ESCALL PERU como empresa dedicada a gestion de cobranzas, seguimiento operativo y reportes.

Problemas principales:

- descarga manual
- limpieza manual
- duplicados
- errores de digitacion
- falta de trazabilidad
- reportes lentos

## 3. Objetivos del proyecto

Objetivo general:

Automatizar la descarga, limpieza, homologacion, validacion, carga y reporte de gestiones usando Python y PostgreSQL/Supabase.

Objetivos especificos:

- conectar a Supabase
- registrar cargas
- limpiar y homologar datos
- evitar duplicados
- registrar logs
- consultar resumen desde vista SQL

## 4. Proceso a automatizar

Mostrar el flujo:

```text
Base de datos / SP -> descarga -> limpieza -> homologacion -> validacion -> duplicados -> carga -> reporte -> logs
```

Explicar que el CSV queda solo como ejemplo, pero el flujo principal ahora usa base de datos.

## 5. Modelo logico: clases, objetos y UML

Mencionar clases principales:

- `Gestion`
- `DescargadorService`
- `LimpiadorService`
- `HomologadorService`
- `ValidadorService`
- `GestionRepository`
- `ReporteService`
- `NotificacionService`

Mostrar `docs/plantuml/clases.puml`.

## 6. Modelo fisico y base de datos

Explicar las tablas:

- `empresas`
- `usuarios`
- `carteras`
- `cargas_gestiones`
- `gestiones`
- `reportes`
- `destinatarios_reportes`
- `envios_reportes`
- `logs_proceso`

Mencionar la vista `vw_resumen_gestiones` y la clave `clave_unica`.

## 7. Codigo fuente y presentacion de automatizacion

Mostrar:

- `app/services`
- `app/repositories`
- `app/main.py`
- `.env.example`
- ejecucion de `python run.py`
- pruebas con `python -m pytest -q`

## 8. Conclusiones y recomendaciones

Conclusiones:

- el proyecto aplica POO
- el proceso ya no depende del CSV
- Supabase centraliza datos y reportes
- los logs mejoran trazabilidad

Recomendaciones:

- implementar Stored Procedure real
- crear tabla staging si se requiere separar datos crudos
- automatizar envio de reportes
- agregar dashboard o programador de tareas

