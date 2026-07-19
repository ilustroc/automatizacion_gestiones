# Modelo lógico

El modelo lógico separa las entidades del dominio de las clases que ejecutan reglas y acceso a datos.

| Clase | Objeto representado | Atributos principales | Métodos principales |
|---|---|---|---|
| `GestionOrigen` | Registro leído de ESCALL | id, fecha, DNI, teléfono, status, tipificación | Construcción tipada mediante `dataclass` |
| `GestionProcesada` | Registro limpio local | originales, homologados, monto, asesor, hash | Representación para persistencia |
| `ControlDescarga` | Ejecución por rango | fechas, tipo, estado, contadores | Estado del proceso |
| `DatabaseConnection` | Sesión MySQL/MariaDB | config, connection | conectar, commit, rollback, ejecutar lote/SP |
| `SourceGestionRepository` | Acceso de lectura a ESCALL | source_db | obtener por rango/lotes, contar, probar SP |
| `GestionProcesadaRepository` | Persistencia local | target_db, batch_size | insertar lote, consultar rango, verificar hash |
| `DescargadorService` | Descarga de origen | source repository | descargar por rango |
| `LimpiadorService` | Normalización de datos | reglas de campos | limpiar DNI/teléfono/dataframe |
| `HomologadorService` | Estandarización | mapas de reglas | homologar status/tipificación |
| `ValidadorService` | Calidad y deduplicación | campos requeridos | validar, generar SHA-256, eliminar duplicados |
| `ProcesadorGestionesService` | Caso de uso principal | repositorios y servicios | procesar control y gestionar transacción |
| `ReportePromesasService` | Alerta del supervisor | repositorio local | consultar, HTML, Excel |
| `ReporteImpulseService` | Reporte de empresa | repositorio local | resumir, detallar, HTML, Excel |
| `ReporteGerenciaService` | Productividad | repositorio local | indicadores, ranking, HTML, Excel |
| `NotificacionService` | Envío SMTP | configuración, repositorio | probar SMTP, enviar HTML/adjunto |

Ejemplo de objetos en ejecución:

```python
source_db = DatabaseConnection(source_config)
target_db = DatabaseConnection(target_config)
descargador = DescargadorService(SourceGestionRepository(source_db))
```

El UML completo está en `docs/plantuml/clases.puml`.
