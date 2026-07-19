# Informe final

## 1. Proyecto

**Automatización del proceso de descarga, limpieza, carga y reporte de gestiones de cobranza**, desarrollado para el curso Lenguajes de Programación y contextualizado en ESCALL PERÚ.

## 2. Paradigma

La solución usa Programación Orientada a Objetos. Clases y objetos distribuyen configuración, acceso a datos, reglas, reportes y notificación. La arquitectura por capas separa presentación, servicios, repositorios, modelos e infraestructura.

## 3. Contexto y problema

ESCALL registra gestiones en `escarperu_software.gestiones`. La preparación manual de información podía introducir errores, duplicados y retrasos. Además, no existía en el proyecto una auditoría integral de descargas y envíos.

## 4. Solución

Se implementaron dos conexiones independientes. La conexión origen ejecuta un SP de lectura por rango. La conexión local administra transacciones y guarda resultados. El flujo limpia DNI, teléfonos, textos, fechas y montos; homologa estados; valida campos; genera SHA-256; inserta por lotes; actualiza controles; genera reportes y registra logs.

ESCALL nunca recibe `INSERT`, `UPDATE` ni `DELETE` desde la aplicación.

## 5. Modelo lógico

Las entidades centrales son `GestionOrigen`, `GestionProcesada`, `ControlDescarga`, `ResultadoProceso`, `Reporte` y `EnvioReporte`. Los repositorios separan origen y destino. `ProcesadorGestionesService` coordina el caso de uso mediante composición.

## 6. Modelo físico

El origen contiene `gestiones` y `sp_descargar_gestiones_rango`. El destino local contiene empresas, usuarios, carteras, controles, cargas, gestiones procesadas, reportes, destinatarios, envíos y logs. Sus vistas producen alertas, detalle e indicadores gerenciales.

## 7. Operación

La aplicación se ejecuta mediante `run.py`. Admite diagnóstico, descarga manual por días u horas, procesamiento de pendientes, última hora automática, interfaz Tkinter y generación/envío de reportes. Dos jobs permiten programar descargas y correos.

## 8. Seguridad

Las credenciales viven en `.env`, excluido de Git. Las contraseñas se escriben entre comillas dobles y no se imprimen. Las consultas usan parámetros. El usuario remoto debe tener privilegios mínimos. El envío real exige `ENVIAR_CORREOS="true"` y `--enviar`.

## 9. Calidad

La suite usa fakes y mocks para configuración, limpieza, homologación, SHA-256, lotes, rollback, rangos, job, reportes y SMTP. No depende de ESCALL, MySQL local ni un correo real.

## 10. Resultados esperados

- menos intervención manual;
- datos estandarizados y sin duplicados;
- ejecución horaria idempotente;
- trazabilidad por control y log;
- reportes oportunos para tres públicos;
- evidencia técnica reproducible para la presentación.

## 11. Limitaciones verificables

Las conexiones reales, el SP, los permisos de cPanel y SMTP solo pueden validarse al configurar credenciales autorizadas. El sistema no afirma conectividad sin ejecutar el diagnóstico.

## 12. Conclusión

El proyecto cumple el objetivo académico mediante una solución profesional por capas que protege la fuente ESCALL y concentra el procesamiento, control y reporte en una base local.
