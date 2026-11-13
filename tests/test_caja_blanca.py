"""
PRUEBAS DE CAJA BLANCA (unittest)
Se diseñan mirando el código de liquidacion/calculos.py para cubrir cada función
del diagrama y cada rama (if/else) al menos una vez.
"""
import unittest
from decimal import Decimal

from liquidacion import calculos as c


class TestFuncionesDelDiagrama(unittest.TestCase):
    def test_calculo_alquiler(self):
        self.assertEqual(c.calculo_alquiler(5, 4), Decimal("700000"))

    def test_calculo_alquiler_adicional(self):
        self.assertEqual(c.calculo_alquiler_adicional(5, 3), Decimal("525000"))

    def test_calculo_alquiler_adicional_cero(self):
        self.assertEqual(c.calculo_alquiler_adicional(5, 0), Decimal("0"))

    def test_calculo_alquiler_adicional_dto(self):
        self.assertEqual(c.calculo_alquiler_adicional_dto(Decimal("525000")), Decimal("10500"))

    # rama if / else de calculo_dentro_establecimiento
    def test_establecimiento_rama_verdadera(self):
        self.assertEqual(c.calculo_dentro_establecimiento(Decimal("1214500"), c.ESTABLECIMIENTO), Decimal("60725"))

    def test_establecimiento_rama_falsa(self):
        self.assertEqual(c.calculo_dentro_establecimiento(Decimal("1214500"), c.FUERA_CIUDAD), Decimal("0"))

    # rama if / else de calculo_domicilio
    def test_domicilio_rama_verdadera(self):
        self.assertEqual(c.calculo_domicilio(Decimal("1214500"), c.FUERA_CIUDAD), Decimal("60725"))

    def test_domicilio_rama_falsa(self):
        self.assertEqual(c.calculo_domicilio(Decimal("1214500"), c.DENTRO_CIUDAD), Decimal("0"))

    def test_calculo_descuento_orden_domicilio_despues_de_descuentos(self):
        dto_ad, dto_est, dom = c.calculo_descuento(Decimal("700000"), Decimal("525000"), c.FUERA_CIUDAD)
        # el 5 % se calcula sobre 1.214.500 (ya descontado el 2 %), no sobre 1.225.000
        self.assertEqual((dto_ad, dto_est, dom), (Decimal("10500"), Decimal("0"), Decimal("60725")))

    def test_redondeo_half_up(self):
        # 2 % de 17.525 = 350,5 -> 351
        self.assertEqual(c.calculo_alquiler_adicional_dto(Decimal("17525")), Decimal("351"))


class TestRamasDeValidacion(unittest.TestCase):
    def test_entero_rechaza_booleano(self):
        with self.assertRaises(TypeError):
            c._entero(True)

    def test_entero_acepta_texto_con_espacios(self):
        self.assertEqual(c._entero(" 7 "), 7)

    def test_entero_acepta_negativo_en_texto(self):
        self.assertEqual(c._entero("-1"), -1)

    def test_entero_rechaza_doble_signo(self):
        with self.assertRaises((TypeError, ValueError)):
            c._entero("--1")

    def test_dias_adicionales_none_es_cero(self):
        self.assertEqual(c.validar_datos("A", 2, 1, None, "CIUDAD")[3], 0)

    def test_validar_normaliza_nombre(self):
        self.assertEqual(c.validar_datos("  Ana  ", "2", "1", "0", "CIUDAD")[0], "Ana")

    def test_mensaje_de_excepcion_contiene_campos(self):
        with self.assertRaises(c.ErrorValidacion) as ctx:
            c.validar_datos("", 2, 1, 0, "CIUDAD")
        self.assertIn("nombre", str(ctx.exception))


class TestLiquidacion(unittest.TestCase):
    def test_a_dict_incluye_texto_modalidad(self):
        d = c.calcular_valores("Ana", 2, 1, 0, "ESTABLECIMIENTO").a_dict()
        self.assertEqual(d["modalidad_texto"], "Dentro del establecimiento")

    def test_total_es_coherente(self):
        l = c.calcular_valores("Ana", 7, 9, 4, "FUERA")
        self.assertEqual(
            l.total,
            l.valor_alquiler + l.valor_adicional_bruto - l.total_descuentos + l.incremento_domicilio,
        )


if __name__ == "__main__":
    unittest.main()
