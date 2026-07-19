# Contexto empresarial

ESCALL PERÚ presta servicios de gestión de cobranzas, seguimiento de contactos y elaboración de reportes operativos para supervisión, empresas contratantes y gerencia. Los asesores registran en el servidor ESCALL el resultado de cada interacción: fecha, DNI, teléfono, estado de contacto, tipificación, observación y, cuando corresponde, promesa de pago.

La operación requiere transformar esos registros en información confiable. El supervisor necesita alertas de promesas; Impulse requiere el detalle de las gestiones realizadas; gerencia necesita medir la productividad diaria de los asesores.

La arquitectura distingue dos responsabilidades:

- La base `escarperu_software` de ESCALL conserva el dato operativo original y se trata como **solo lectura**.
- La base local `automatizacion_gestiones` conserva datos limpios, controles, auditoría y resultados del proyecto.

Esta separación protege la operación de ESCALL y permite que el proyecto procese, reporte y audite sin alterar la fuente oficial.
