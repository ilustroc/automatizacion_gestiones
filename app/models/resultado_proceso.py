from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ResultadoProceso:
    id_control: int
    registros_origen: int
    registros_insertados: int
    registros_duplicados: int
    registros_invalidos: int

    def como_dict(self) -> dict[str, int]:
        return {
            "id_control": self.id_control,
            "leidos": self.registros_origen,
            "insertados": self.registros_insertados,
            "duplicados": self.registros_duplicados,
            "descartados": self.registros_invalidos,
        }
