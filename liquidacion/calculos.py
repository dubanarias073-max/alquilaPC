"""
Reglas de negocio de ALQUILAPC (sin base de datos).

Estructura de funciones según el diagrama del taller:

    calcular_valores()
     ├── calculo_alquiler()
     ├── calculo_alquiler_adicional()
     └── calculo_descuento()
          ├── calculo_alquiler_adicional_dto()
          ├── calculo_dentro_establecimiento()
          └── calculo_domicilio()

Reglas (RN):
    RN01  $35.000 por equipo por día.
    RN02  Mínimo 2 equipos.
    RN03  Modalidades: dentro de la ciudad, fuera de la ciudad, dentro del establecimiento.
    RN04  Fuera de la ciudad: incremento del 5 % aplicado después de los descuentos.
    RN05  Dentro del establecimiento: descuento del 5 % sobre el total.
    RN06  Días adicionales: descuento del 2 % sobre el total de los días adicionales.
    RN07  El recibo contiene nombre, modalidad, equipos, días, descuentos, incrementos y total.
"""
from dataclasses import dataclass, asdict
from decimal import Decimal, ROUND_HALF_UP

VALOR_DIA = Decimal("35000")
MIN_EQUIPOS = 2
MAX_NOMBRE = 100
PORC_DTO_ADICIONAL = Decimal("0.02")
PORC_DTO_ESTABLECIMIENTO = Decimal("0.05")
PORC_DOMICILIO = Decimal("0.05")

DENTRO_CIUDAD = "CIUDAD"
FUERA_CIUDAD = "FUERA"
ESTABLECIMIENTO = "ESTABLECIMIENTO"

MODALIDADES = {
    DENTRO_CIUDAD: "Dentro de la ciudad",
    FUERA_CIUDAD: "Fuera de la ciudad",
    ESTABLECIMIENTO: "Dentro del establecimiento",
}


class ErrorValidacion(ValueError):
    """Se lanza cuando los datos de entrada no cumplen las reglas (PBI014)."""

    def __init__(self, errores):
        self.errores = errores
        super().__init__("; ".join(f"{k}: {v}" for k, v in errores.items()))


def _pesos(valor):
    """Redondea a pesos enteros (half-up)."""
    return Decimal(valor).quantize(Decimal("1"), rounding=ROUND_HALF_UP)


def _entero(valor):
    """Convierte a int sin aceptar decimales, booleanos ni texto no numérico."""
    if isinstance(valor, bool):
        raise TypeError
    if isinstance(valor, int):
        return valor
    texto = str(valor).strip()
    if not texto.lstrip("-").isdigit():
        raise TypeError
    return int(texto)


def validar_datos(nombre, equipos, dias_iniciales, dias_adicionales, modalidad):
    """Valida y normaliza la entrada. Devuelve una tupla con los valores limpios."""
    errores = {}

    nombre = (nombre or "").strip()
    if not nombre:
        errores["nombre"] = "El nombre del cliente es obligatorio."
    elif len(nombre) > MAX_NOMBRE:  # H-03: antes solo se limitaba en el HTML
        errores["nombre"] = f"El nombre no puede superar {MAX_NOMBRE} caracteres."

    try:
        equipos = _entero(equipos)
        if equipos < MIN_EQUIPOS:
            errores["equipos"] = f"La cantidad mínima es de {MIN_EQUIPOS} equipos."
    except (TypeError, ValueError):
        errores["equipos"] = "La cantidad de equipos debe ser un número entero."

    try:
        dias_iniciales = _entero(dias_iniciales)
        if dias_iniciales <= 0:
            errores["dias_iniciales"] = "Los días iniciales deben ser mayores a cero."
    except (TypeError, ValueError):
        errores["dias_iniciales"] = "Los días iniciales deben ser un número entero."

    if dias_adicionales in (None, ""):
        dias_adicionales = 0
    try:
        dias_adicionales = _entero(dias_adicionales)
        if dias_adicionales < 0:
            errores["dias_adicionales"] = "Los días adicionales no pueden ser negativos."
    except (TypeError, ValueError):
        errores["dias_adicionales"] = "Los días adicionales deben ser un número entero."

    if modalidad not in MODALIDADES:
        errores["modalidad"] = "Seleccione una modalidad válida."

    if errores:
        raise ErrorValidacion(errores)
    return nombre, equipos, dias_iniciales, dias_adicionales, modalidad


# ---------------------------------------------------------------- cálculos
def calculo_alquiler(equipos, dias_iniciales):
    """Valor base: equipos x días iniciales x $35.000 (RN01)."""
    return _pesos(equipos * dias_iniciales * VALOR_DIA)


def calculo_alquiler_adicional(equipos, dias_adicionales):
    """Valor bruto de los días adicionales: equipos x días adicionales x $35.000."""
    return _pesos(equipos * dias_adicionales * VALOR_DIA)


def calculo_alquiler_adicional_dto(valor_adicional):
    """2 % sobre el total de los días adicionales (RN06)."""
    return _pesos(valor_adicional * PORC_DTO_ADICIONAL)


def calculo_dentro_establecimiento(subtotal, modalidad):
    """5 % sobre el total si el servicio es en el establecimiento (RN05)."""
    if modalidad == ESTABLECIMIENTO:
        return _pesos(subtotal * PORC_DTO_ESTABLECIMIENTO)
    return Decimal("0")


def calculo_domicilio(valor_despues_descuentos, modalidad):
    """5 % de cargo fuera de la ciudad, aplicado después de descuentos (RN04)."""
    if modalidad == FUERA_CIUDAD:
        return _pesos(valor_despues_descuentos * PORC_DOMICILIO)
    return Decimal("0")


def calculo_descuento(valor_alquiler, valor_adicional, modalidad):
    """Orquesta descuentos e incremento en el orden de las reglas de negocio."""
    dto_adicional = calculo_alquiler_adicional_dto(valor_adicional)
    subtotal = valor_alquiler + valor_adicional - dto_adicional
    dto_establecimiento = calculo_dentro_establecimiento(subtotal, modalidad)
    domicilio = calculo_domicilio(subtotal - dto_establecimiento, modalidad)
    return dto_adicional, dto_establecimiento, domicilio


@dataclass
class Liquidacion:
    nombre: str
    equipos: int
    dias_iniciales: int
    dias_adicionales: int
    modalidad: str
    valor_alquiler: Decimal
    valor_adicional_bruto: Decimal
    descuento_adicional: Decimal
    descuento_establecimiento: Decimal
    total_descuentos: Decimal
    incremento_domicilio: Decimal
    total: Decimal

    @property
    def modalidad_texto(self):
        return MODALIDADES[self.modalidad]

    @property
    def valor_adicional_neto(self):
        return self.valor_adicional_bruto - self.descuento_adicional

    def a_dict(self):
        datos = asdict(self)
        datos["modalidad_texto"] = self.modalidad_texto
        return datos


def calcular_valores(nombre, equipos, dias_iniciales, dias_adicionales, modalidad):
    """Punto de entrada: valida, calcula y devuelve la Liquidacion (factura)."""
    nombre, equipos, dias_iniciales, dias_adicionales, modalidad = validar_datos(
        nombre, equipos, dias_iniciales, dias_adicionales, modalidad
    )
    valor_alquiler = calculo_alquiler(equipos, dias_iniciales)
    valor_adicional = calculo_alquiler_adicional(equipos, dias_adicionales)
    dto_adicional, dto_establecimiento, domicilio = calculo_descuento(
        valor_alquiler, valor_adicional, modalidad
    )
    total_descuentos = dto_adicional + dto_establecimiento
    total = valor_alquiler + valor_adicional - total_descuentos + domicilio
    return Liquidacion(
        nombre=nombre,
        equipos=equipos,
        dias_iniciales=dias_iniciales,
        dias_adicionales=dias_adicionales,
        modalidad=modalidad,
        valor_alquiler=valor_alquiler,
        valor_adicional_bruto=valor_adicional,
        descuento_adicional=dto_adicional,
        descuento_establecimiento=dto_establecimiento,
        total_descuentos=total_descuentos,
        incremento_domicilio=domicilio,
        total=total,
    )
