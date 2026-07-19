import re
import unicodedata
from decimal import Decimal


def solo_numeros(valor: object) -> str:
    if valor is None:
        return ""
    if isinstance(valor, float) and valor.is_integer():
        valor = int(valor)
    if isinstance(valor, Decimal) and valor == valor.to_integral_value():
        valor = valor.to_integral_value()
    return re.sub(r"\D", "", str(valor))


def limpiar_espacios(valor: object) -> str:
    if valor is None:
        return ""
    return " ".join(str(valor).strip().split())


def normalizar_texto(valor: object) -> str:
    texto = limpiar_espacios(valor).upper()
    texto = unicodedata.normalize("NFKD", texto)
    return "".join(caracter for caracter in texto if not unicodedata.combining(caracter))
