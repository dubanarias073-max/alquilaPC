"""
PRUEBAS DE REGRESIÓN
Valores "dorados" ya aprobados. Si un cambio en el código altera cualquiera de
estos totales, la suite falla y se sabe que se rompió algo que antes funcionaba.
Se ejecutan después de cada corrección (ver informe de hallazgos).
"""
import unittest
from decimal import Decimal

from liquidacion.calculos import calcular_valores

# (equipos, dias, adicionales, modalidad) -> (descuentos, domicilio, total)
CASOS_APROBADOS = {
    (5, 4, 3, "CIUDAD"): (10500, 0, 1214500),
    (5, 4, 3, "FUERA"): (10500, 60725, 1275225),
    (5, 4, 3, "ESTABLECIMIENTO"): (71225, 0, 1153775),
    (2, 1, 0, "CIUDAD"): (0, 0, 70000),
    (2, 1, 0, "FUERA"): (0, 3500, 73500),
    (2, 1, 0, "ESTABLECIMIENTO"): (3500, 0, 66500),
    (2, 3, 0, "FUERA"): (0, 10500, 220500),
    (5, 10, 0, "ESTABLECIMIENTO"): (87500, 0, 1662500),
    (2, 1, 2, "CIUDAD"): (2800, 0, 207200),
    (10, 30, 10, "ESTABLECIMIENTO"): (766500, 0, 13233500),
    (3, 2, 1, "FUERA"): (2100, 15645, 328545),
    (2, 2, 1, "ESTABLECIMIENTO"): (11830, 0, 198170),
}


class TestRegresion(unittest.TestCase):
    def test_casos_aprobados_no_cambian(self):
        for (eq, dias, ad, mod), (dto, dom, total) in CASOS_APROBADOS.items():
            with self.subTest(equipos=eq, dias=dias, adicionales=ad, modalidad=mod):
                l = calcular_valores("Regresión", eq, dias, ad, mod)
                self.assertEqual(l.total_descuentos, Decimal(dto))
                self.assertEqual(l.incremento_domicilio, Decimal(dom))
                self.assertEqual(l.total, Decimal(total))

    def test_hallazgo_h01_descuento_adicional_no_es_por_dia(self):
        """H-01: el 2 % es sobre el total de días adicionales, no 2 % x cada día."""
        l = calcular_valores("Reg", 5, 4, 3, "CIUDAD")
        self.assertEqual(l.descuento_adicional, Decimal("10500"))  # no 31.500 (6 %)

    def test_hallazgo_h02_domicilio_sobre_valor_con_descuento(self):
        """H-02: el 5 % de domicilio se calcula después del descuento del 2 %."""
        l = calcular_valores("Reg", 5, 4, 3, "FUERA")
        self.assertEqual(l.incremento_domicilio, Decimal("60725"))  # no 61.250

    def test_hallazgo_h03_nombre_maximo_100(self):
        """H-03: el backend debe rechazar nombres de más de 100 caracteres."""
        from liquidacion.calculos import ErrorValidacion
        with self.assertRaises(ErrorValidacion):
            calcular_valores("A" * 150, 2, 1, 0, "CIUDAD")


if __name__ == "__main__":
    unittest.main()
