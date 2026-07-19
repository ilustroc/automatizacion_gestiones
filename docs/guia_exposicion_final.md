# Guía de exposición final

Duración objetivo: 5 a 7 minutos. Practicar una explicación de 35 a 50 segundos por vista.

## Vista 1. Paradigma de programación

“Usamos Programación Orientada a Objetos. Cada responsabilidad está encapsulada en clases de configuración, repositorios y servicios. También aplicamos arquitectura por capas, lo que permite probar la lógica sin conectarnos a servidores reales.”

Mostrar `docs/plantuml/clases.puml`.

## Vista 2. Contexto y problemática

“ESCALL PERÚ gestiona cobranzas y necesita entregar información a supervisión, Impulse y gerencia. El proceso manual ocasionaba demoras, formatos inconsistentes, duplicados y poca trazabilidad.”

## Vista 3. Objetivos

“El objetivo general es automatizar desde la descarga hasta el reporte. Los objetivos específicos incluyen conexión segura, limpieza, homologación, SHA-256, carga local, auditoría y tres reportes.”

## Vista 4. Proceso a automatizar

“ESCALL es origen de solo lectura. Un Stored Procedure entrega un rango; Python limpia, valida y deduplica; la base local guarda resultados; las vistas alimentan reportes y correo.”

Mostrar `docs/plantuml/flujo_proceso.puml`.

## Vista 5. Modelo lógico y UML

“`SourceGestionRepository` consulta ESCALL; `ProcesadorGestionesService` coordina reglas; `GestionProcesadaRepository` inserta por lotes; los servicios de reporte y notificación consumen únicamente el destino local.”

## Vista 6. Modelo físico

“Hay dos bases. ESCALL conserva `gestiones` y el SP. Local contiene controles, gestiones procesadas, reportes, envíos y logs. La clave única es un SHA-256 de 64 caracteres.”

Mostrar phpMyAdmin y `docs/plantuml/modelo_relacional.puml`.

## Vista 7. Código y automatización

“La CLI admite diagnóstico, manual, pendientes, automático, interfaz y reportes. El job toma la última hora cerrada; por ejemplo, a las 18:05 procesa de 17:00 a 18:00.”

Mostrar diagnóstico, ejecución, filas locales y pruebas.

## Vista 8. Conclusiones y recomendaciones

“La solución reduce trabajo repetitivo, conserva trazabilidad y evita duplicados sin alterar ESCALL. Recomendamos permisos mínimos, copias de seguridad, monitoreo y futura parametrización de reglas.”

Cerrar mostrando los tres reportes y aclarar que los correos reales requieren `--enviar`.

## Preguntas probables

- **¿Por qué dos bases?** Para no alterar la fuente operativa y aislar el procesamiento académico.
- **¿Cómo evita duplicados?** SHA-256, índice único e `INSERT IGNORE`.
- **¿Qué ocurre si falla?** Rollback local, control `ERROR`, log técnico y cierre de conexiones.
- **¿El CSV sigue siendo necesario?** No; solo se conserva como evidencia en `data/examples`.
- **¿Las pruebas envían correos?** No; usan SMTP simulado.
