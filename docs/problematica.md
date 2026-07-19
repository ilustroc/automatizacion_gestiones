# Problemática

El proceso anterior requería descargar información, revisar formatos, corregir DNI y teléfonos, homologar estados, eliminar duplicados, consolidar resultados y preparar reportes manualmente.

Sus principales riesgos eran:

- tiempo operativo dedicado a tareas repetitivas;
- errores de digitación y formatos inconsistentes;
- duplicados al reprocesar rangos;
- pérdida de ceros iniciales del DNI;
- reportes tardíos para supervisor, Impulse y gerencia;
- ausencia de un control central de ejecuciones;
- dificultad para conocer el origen de un error;
- falta de trazabilidad de correos y reportes.

El proyecto resuelve el problema con rangos de fecha y hora, Stored Procedure parametrizado, reglas de limpieza y homologación, hash SHA-256, transacciones, vistas locales, reportes automáticos y logs de auditoría.
