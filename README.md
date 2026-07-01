# automatizacion-gestiones-cobranza

Proyecto en Python para automatizar la descarga, limpieza, homologacion, depuracion y reporte de gestiones de cobranza.

## Problema que resuelve

En procesos operativos de cobranza suelen recibirse archivos con datos repetidos, telefonos con formatos diferentes, estados escritos de varias formas y fechas inconsistentes. Este proyecto prepara esos datos para obtener un archivo limpio y dejar lista la estructura para futuras cargas a base de datos y envio de reportes.

## Estructura del proyecto

```text
app/
  main.py
  config.py
  models/
  services/
  repositories/
  utils/
data/
  input/
  output/
docs/
  plantuml/
logs/
tests/
run.py
```

## Instalacion

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Como ejecutar

```bash
python run.py
```

El proceso lee `data/input/gestiones.csv` y genera `data/output/gestiones_limpias.xlsx`.

## Campos usados

- `fecha_gestion`
- `dni`
- `telefono`
- `status`
- `tipificacion`
- `observacion`
- `fecha_pago`
- `monto_pago`
- `nombre`

## Flujo del proceso

1. Leer archivo CSV.
2. Validar columnas requeridas.
3. Limpiar DNI, telefono, textos, fechas y montos.
4. Homologar status y tipificacion.
5. Eliminar duplicados usando una clave compuesta.
6. Exportar el resultado a Excel.
7. Registrar resumen y logs basicos.

## Explicacion de carpetas

- `app/models`: clases principales del sistema.
- `app/services`: logica de negocio para limpieza, homologacion, validacion y reportes.
- `app/repositories`: estructura preparada para carga futura a base de datos.
- `app/utils`: funciones reutilizables para texto y fechas.
- `data/input`: archivos de entrada.
- `data/output`: archivos generados.
- `docs`: documentacion tecnica y diagramas.
- `logs`: archivo de log de ejecucion.
- `tests`: pruebas basicas del proyecto.

## Reglas principales

- `dni` y `telefono` quedan solo con numeros.
- `status` y `tipificacion` se convierten a mayusculas y se homologan.
- `ILOCALIZADO` en status se considera `NO CONTACTO`, porque no hubo contacto efectivo.
- Los duplicados se eliminan con la clave: `dni + telefono + fecha_gestion + status + tipificacion`.

## Proximas mejoras

- Cargar gestiones limpias en PostgreSQL/Supabase.
- Registrar ejecuciones en base de datos.
- Generar reportes por empresa o fecha.
- Enviar reportes por correo.
- Agregar validaciones adicionales de negocio.

