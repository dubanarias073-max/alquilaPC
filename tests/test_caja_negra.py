"""
PRUEBAS DE CAJA NEGRA (unittest)
Se diseñan solo con los requisitos: partición de equivalencia, valores límite,
tabla de decisión por modalidad. No miran el código interno.
"""
import unittest
from decimal import Decimal

from liquidacion.calculos import ErrorValidacion, calcular_valores


class TestTablaReferenciaTaller(unittest.TestCase):
    """Valores de la hoja de referencia del taller: 5 equipos, 4 días, 3 adicionales."""

    def test_cn01_en_la_ciudad(self):
        l = calcular_valores("Juan", 5, 4, 3, "CIUDAD")
        self.assertEqual(l.valor_alquiler, Decimal("700000"))
        self.assertEqual(l.valor_adicional_neto, Decimal("514500"))
        self.assertEqual(l.total_descuentos, Decimal("10500"))
        self.assertEqual(l.incremento_domicilio, Decimal("0"))
        self.assertEqual(l.total, Decimal("1214500"))

    def test_cn02_fuera_de_la_ciudad(self):
        l = calcular_valores("Juan", 5, 4, 3, "FUERA")
        self.assertEqual(l.total_descuentos, Decimal("10500"))
        self.assertEqual(l.incremento_domicilio, Decimal("60725"))
        self.assertEqual(l.total, Decimal("1275225"))

    def test_cn03_en_el_establecimiento(self):
        l = calcular_valores("Juan", 5, 4, 3, "ESTABLECIMIENTO")
        self.assertEqual(l.total_descuentos, Decimal("71225"))
        self.assertEqual(l.incremento_domicilio, Decimal("0"))
        self.assertEqual(l.total, Decimal("1153775"))


class TestEscenariosPlan(unittest.TestCase):
    """Escenarios S01-S05 del plan de pruebas."""

    def test_s01_2_equipos_1_dia_ciudad(self):
        self.assertEqual(calcular_valores("Juan", 2, 1, 0, "CIUDAD").total, Decimal("70000"))

    def test_s02_2_equipos_3_dias_fuera(self):
        # 210000 + 5 % = 220500
        self.assertEqual(calcular_valores("Ana", 2, 3, 0, "FUERA").total, Decimal("220500"))

    def test_s03_5_equipos_10_dias_establecimiento(self):
        # 1.750.000 - 5 % (87.500) = 1.662.500
        self.assertEqual(calcular_valores("María", 5, 10, 0, "ESTABLECIMIENTO").total, Decimal("1662500"))

    def test_s04_con_dias_adicionales(self):
        # base 70.000 + adicional 140.000 - 2 % (2.800) = 207.200
        l = calcular_valores("Pedro", 2, 1, 2, "CIUDAD")
        self.assertEqual(l.descuento_adicional, Decimal("2800"))
        self.assertEqual(l.total, Decimal("207200"))

    def test_s05_maximo_descuento_establecimiento_con_adicionales(self):
        # 10 eq, 30 días, 10 adic, establecimiento: ambos descuentos a la vez
        l = calcular_valores("Pedro", 10, 30, 10, "ESTABLECIMIENTO")
        self.assertEqual(l.valor_alquiler, Decimal("10500000"))
        self.assertEqual(l.descuento_adicional, Decimal("70000"))
        # subtotal = 10.500.000 + 3.500.000 - 70.000 = 13.930.000 ; 5 % = 696.500
        self.assertEqual(l.descuento_establecimiento, Decimal("696500"))
        self.assertEqual(l.total, Decimal("13233500"))


class TestParticionesYLimites(unittest.TestCase):
    def _error(self, **kw):
        datos = dict(nombre="Juan", equipos=2, dias_iniciales=1, dias_adicionales=0, modalidad="CIUDAD")
        datos.update(kw)
        with self.assertRaises(ErrorValidacion) as ctx:
            calcular_valores(**datos)
        return ctx.exception.errores

    # Nombre
    def test_nombre_vacio(self):
        self.assertIn("nombre", self._error(nombre=""))

    def test_nombre_solo_espacios(self):
        self.assertIn("nombre", self._error(nombre="   "))

    def test_nombre_100_caracteres_valido(self):
        self.assertEqual(len(calcular_valores("A" * 100, 2, 1, 0, "CIUDAD").nombre), 100)

    def test_nombre_101_caracteres_invalido(self):
        self.assertIn("nombre", self._error(nombre="A" * 101))

    # Equipos: límites 1 | 2 | 3
    def test_equipos_0(self):
        self.assertIn("equipos", self._error(equipos=0))

    def test_equipos_1_limite_invalido(self):
        self.assertIn("equipos", self._error(equipos=1))

    def test_equipos_2_limite_valido(self):
        self.assertEqual(calcular_valores("Juan", 2, 1, 0, "CIUDAD").equipos, 2)

    def test_equipos_3_valido(self):
        self.assertEqual(calcular_valores("Juan", 3, 1, 0, "CIUDAD").total, Decimal("105000"))

    def test_equipos_texto(self):
        self.assertIn("equipos", self._error(equipos="abc"))

    def test_equipos_decimal(self):
        self.assertIn("equipos", self._error(equipos="2.5"))

    # Días iniciales: 0 | 1
    def test_dias_iniciales_0(self):
        self.assertIn("dias_iniciales", self._error(dias_iniciales=0))

    def test_dias_iniciales_negativo(self):
        self.assertIn("dias_iniciales", self._error(dias_iniciales=-3))

    def test_dias_iniciales_1_valido(self):
        self.assertEqual(calcular_valores("Juan", 2, 1, 0, "CIUDAD").dias_iniciales, 1)

    # Días adicionales: -1 | 0 | 1
    def test_dias_adicionales_menos_1(self):
        self.assertIn("dias_adicionales", self._error(dias_adicionales=-1))

    def test_dias_adicionales_0_sin_descuento(self):
        self.assertEqual(calcular_valores("Juan", 2, 1, 0, "CIUDAD").descuento_adicional, Decimal("0"))

    def test_dias_adicionales_1(self):
        # 70.000 * 2 % = 1.400
        self.assertEqual(calcular_valores("Juan", 2, 1, 1, "CIUDAD").descuento_adicional, Decimal("1400"))

    def test_dias_adicionales_vacio_equivale_a_cero(self):
        self.assertEqual(calcular_valores("Juan", 2, 1, "", "CIUDAD").dias_adicionales, 0)

    # Modalidad
    def test_modalidad_invalida_4(self):
        self.assertIn("modalidad", self._error(modalidad="4"))

    def test_modalidad_vacia(self):
        self.assertIn("modalidad", self._error(modalidad=""))

    def test_varios_errores_a_la_vez(self):
        errores = self._error(nombre="", equipos=1, dias_iniciales=0, dias_adicionales=-1, modalidad="X")
        self.assertEqual(set(errores), {"nombre", "equipos", "dias_iniciales", "dias_adicionales", "modalidad"})


if __name__ == "__main__":
    unittest.main()
