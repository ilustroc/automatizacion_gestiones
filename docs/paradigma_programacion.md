# Paradigma de programación

El proyecto usa **Programación Orientada a Objetos (POO)** porque el proceso reúne responsabilidades distintas que necesitan evolucionar sin mezclarse: conexión, descarga, limpieza, validación, persistencia, reportes y correo.

Una **clase** define estructura y comportamiento; por ejemplo, `DatabaseConnection` define cómo abrir, confirmar y revertir una conexión. Un **objeto** es una instancia concreta, como `source_db` configurado para ESCALL o `target_db` configurado para el servidor local. Los **atributos** conservan estado, como `host`, `batch_size` o `estado`. Los **métodos** ejecutan acciones, como `obtener_gestiones_por_rango()`, `insertar_lote()` o `enviar_html()`.

Principios aplicados:

- **Encapsulamiento:** las credenciales y detalles de PyMySQL quedan en configuración y conexión.
- **Abstracción:** los servicios trabajan con repositorios sin incorporar SQL directamente.
- **Composición:** `ProcesadorGestionesService` coordina objetos especializados.
- **Responsabilidad única:** cada clase atiende una parte concreta del flujo.
- **Polimorfismo práctico:** los tests sustituyen repositorios y SMTP por objetos fake con la misma interfaz.

La POO se complementa con una organización modular por capas:

```text
presentación (CLI/Tkinter/jobs)
-> servicios
-> repositorios
-> modelos y utilidades
-> MySQL origen/destino y SMTP
```

Esta combinación mejora legibilidad, pruebas, mantenimiento, seguridad y trazabilidad, criterios relevantes para una automatización académica y empresarial.
