# Código fuente

## Estructura

```text
automatizacion_gestiones/
├── app/
│   ├── models/          dataclasses del dominio
│   ├── repositories/    origen ESCALL y destino local
│   ├── services/        procesamiento, diagnóstico, reportes y SMTP
│   ├── ui/              ventana Tkinter
│   └── utils/           texto y fechas
├── data/
│   ├── examples/        CSV histórico, no operativo
│   └── output/          Excel opcional
├── docs/
│   ├── sql/             scripts de origen, esquema y vistas
│   └── plantuml/        diagramas
├── jobs/                descarga horaria y reportes
├── tests/               mocks y fakes sin servicios reales
├── run.py               punto de entrada
├── requirements.txt     dependencias compatibles
└── .env.example         plantilla sin secretos
```

## Archivos clave

- `app/config.py`: valida dos bases, SMTP, destinatarios y opciones generales.
- `app/repositories/database.py`: conexión reusable, context manager y transacciones.
- `source_schema_repository.py`: diagnóstico de tabla, columnas, versión y SP.
- `source_gestion_repository.py`: consultas de solo lectura a ESCALL.
- `gestion_procesada_repository.py`: inserción local por lotes con `INSERT IGNORE`.
- `procesador_gestiones_service.py`: coordina el caso de uso y el rollback.
- `app/main.py`: argumentos, composición de dependencias y comandos.
- `app/ui/descargas_view.py`: selección visual de fechas y horas.

## Comandos de referencia

```powershell
python run.py --modo diagnostico
python run.py --modo manual --fecha-inicio 2026-07-01 --fecha-fin 2026-07-18
python run.py --modo pendiente
python run.py --interfaz
python run.py --reporte todos --solo-generar
python -m pytest -q
```

El SQL permanece en los repositorios; `app/main.py` solo coordina dependencias y casos de uso.
