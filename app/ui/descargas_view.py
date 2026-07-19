import tkinter as tk
from datetime import datetime, timedelta
from tkinter import messagebox, ttk
from typing import Callable


class DescargasView:
    def __init__(
        self,
        probar_conexiones: Callable[[], str],
        registrar_descarga: Callable[[datetime, datetime, str, str], str],
        ejecutar_descarga: Callable[[datetime, datetime, str, str], str],
        consultar_ultimas: Callable[[], list[dict]],
    ):
        self.probar_conexiones = probar_conexiones
        self.registrar_descarga = registrar_descarga
        self.ejecutar_descarga = ejecutar_descarga
        self.consultar_ultimas = consultar_ultimas
        self.root = tk.Tk()
        self.root.title("Automatización de gestiones de cobranza")
        self.root.resizable(False, False)
        self._crear_variables()
        self._crear_controles()

    def _crear_variables(self) -> None:
        ahora = datetime.now().replace(second=0, microsecond=0)
        fin = ahora + timedelta(hours=1)
        self.fecha_desde = tk.StringVar(value=ahora.strftime("%Y-%m-%d"))
        self.hora_desde = tk.StringVar(value=ahora.strftime("%H:%M"))
        self.fecha_hasta = tk.StringVar(value=fin.strftime("%Y-%m-%d"))
        self.hora_hasta = tk.StringVar(value=fin.strftime("%H:%M"))
        self.tipo = tk.StringVar(value="MANUAL")
        self.descripcion = tk.StringVar(value="Descarga registrada desde la interfaz")

    def _crear_controles(self) -> None:
        marco = ttk.Frame(self.root, padding=16)
        marco.grid(sticky="nsew")
        campos = [
            ("Fecha desde (YYYY-MM-DD)", self.fecha_desde),
            ("Hora desde (HH:MM)", self.hora_desde),
            ("Fecha hasta (YYYY-MM-DD)", self.fecha_hasta),
            ("Hora hasta (HH:MM)", self.hora_hasta),
        ]
        for fila, (etiqueta, variable) in enumerate(campos):
            ttk.Label(marco, text=etiqueta).grid(
                row=fila, column=0, sticky="w", padx=(0, 12), pady=4
            )
            ttk.Entry(marco, textvariable=variable, width=28).grid(
                row=fila, column=1, sticky="ew", pady=4
            )

        ttk.Label(marco, text="Tipo de descarga").grid(
            row=4, column=0, sticky="w", padx=(0, 12), pady=4
        )
        ttk.Combobox(
            marco,
            textvariable=self.tipo,
            values=("MANUAL", "AUTOMATICA"),
            state="readonly",
            width=25,
        ).grid(row=4, column=1, sticky="ew", pady=4)
        ttk.Label(marco, text="Descripción").grid(
            row=5, column=0, sticky="w", padx=(0, 12), pady=4
        )
        ttk.Entry(marco, textvariable=self.descripcion, width=42).grid(
            row=5, column=1, sticky="ew", pady=4
        )

        botones = ttk.Frame(marco)
        botones.grid(row=6, column=0, columnspan=2, pady=(14, 0), sticky="ew")
        acciones = [
            ("Probar conexiones", self._probar),
            ("Registrar descarga pendiente", self._registrar),
            ("Ejecutar descarga ahora", self._ejecutar),
            ("Consultar últimas ejecuciones", self._consultar),
            ("Cerrar", self.root.destroy),
        ]
        for indice, (texto, comando) in enumerate(acciones):
            ttk.Button(botones, text=texto, command=comando).grid(
                row=indice // 2,
                column=indice % 2,
                sticky="ew",
                padx=3,
                pady=3,
            )
        botones.columnconfigure(0, weight=1)
        botones.columnconfigure(1, weight=1)

    def run(self) -> None:
        self.root.mainloop()

    def _obtener_datos(self) -> tuple[datetime, datetime, str, str]:
        try:
            desde = datetime.strptime(
                f"{self.fecha_desde.get()} {self.hora_desde.get()}",
                "%Y-%m-%d %H:%M",
            )
            hasta = datetime.strptime(
                f"{self.fecha_hasta.get()} {self.hora_hasta.get()}",
                "%Y-%m-%d %H:%M",
            )
        except ValueError as error:
            raise ValueError(
                "Use fecha YYYY-MM-DD y hora HH:MM en todos los campos."
            ) from error
        if hasta <= desde:
            raise ValueError("La fecha y hora final debe ser mayor que la inicial.")
        descripcion = self.descripcion.get().strip()
        if not descripcion:
            raise ValueError("La descripción es obligatoria.")
        return desde, hasta, self.tipo.get(), descripcion

    def _probar(self) -> None:
        self._ejecutar_accion(self.probar_conexiones)

    def _registrar(self) -> None:
        self._ejecutar_accion(lambda: self.registrar_descarga(*self._obtener_datos()))

    def _ejecutar(self) -> None:
        self._ejecutar_accion(lambda: self.ejecutar_descarga(*self._obtener_datos()))

    def _consultar(self) -> None:
        def accion() -> str:
            filas = self.consultar_ultimas()
            if not filas:
                return "No hay ejecuciones registradas."
            return "\n".join(
                f"#{fila['id_control']} | {fila['estado']} | "
                f"{fila['fecha_desde']} -> {fila['fecha_hasta']}"
                for fila in filas
            )

        self._ejecutar_accion(accion)

    @staticmethod
    def _ejecutar_accion(accion: Callable[[], str]) -> None:
        try:
            messagebox.showinfo("Automatización de gestiones", accion())
        except Exception as error:
            messagebox.showerror("No se pudo completar la acción", str(error))
