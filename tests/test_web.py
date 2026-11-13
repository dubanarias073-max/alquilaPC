"""
PRUEBAS DE INTEGRACIÓN / SISTEMA sobre la aplicación web (sin base de datos).
Se ejecutan con:  python manage.py test tests
"""
from django.test import SimpleTestCase
from django.urls import reverse

from liquidacion.repositorio import repositorio

VALIDO = {
    "nombre": "Juan Pérez",
    "equipos": "5",
    "dias_iniciales": "4",
    "dias_adicionales": "3",
    "modalidad": "FUERA",
}


class TestWeb(SimpleTestCase):
    def setUp(self):
        repositorio.limpiar()

    def test_pagina_principal_responde(self):
        r = self.client.get(reverse("liquidacion:inicio"))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Liquidar servicio")
        self.assertContains(r, "Dentro del establecimiento")

    def test_liquidar_redirige_al_recibo(self):
        r = self.client.post(reverse("liquidacion:liquidar"), VALIDO)
        self.assertRedirects(r, reverse("liquidacion:recibo", args=[1]))

    def test_recibo_contiene_datos_rn07(self):
        self.client.post(reverse("liquidacion:liquidar"), VALIDO)
        r = self.client.get(reverse("liquidacion:recibo", args=[1]))
        for texto in ("Juan Pérez", "Fuera de la ciudad", "$700.000", "$525.000",
                      "$10.500", "$60.725", "$1.275.225", "Imprimir recibo"):
            self.assertContains(r, texto)

    def test_consultar_servicio_existente(self):
        self.client.post(reverse("liquidacion:liquidar"), VALIDO)
        r = self.client.get(reverse("liquidacion:consultar"), {"numero": "1"})
        self.assertRedirects(r, reverse("liquidacion:recibo", args=[1]))

    def test_consultar_servicio_inexistente(self):
        r = self.client.get(reverse("liquidacion:consultar"), {"numero": "99"})
        self.assertEqual(r.status_code, 404)
        self.assertContains(r, "No existe un servicio", status_code=404)

    def test_consultar_sin_numero(self):
        r = self.client.get(reverse("liquidacion:consultar"))
        self.assertEqual(r.status_code, 400)

    def test_recibo_inexistente_404(self):
        self.assertEqual(self.client.get("/servicio/123/").status_code, 404)

    def test_datos_invalidos_no_generan_recibo(self):
        datos = dict(VALIDO, nombre="", equipos="1", dias_iniciales="0", dias_adicionales="-1", modalidad="4")
        r = self.client.post(reverse("liquidacion:liquidar"), datos)
        self.assertEqual(r.status_code, 400)
        for msg in ("El nombre del cliente es obligatorio", "La cantidad mínima es de 2 equipos",
                    "mayores a cero", "no pueden ser negativos", "Seleccione una modalidad"):
            self.assertContains(r, msg, status_code=400)
        self.assertEqual(repositorio.listar(), [])

    def test_formulario_conserva_datos_tras_error(self):
        r = self.client.post(reverse("liquidacion:liquidar"), dict(VALIDO, equipos="1"))
        self.assertContains(r, 'value="Juan Pérez"', status_code=400)

    def test_liquidar_por_get_no_permitido(self):
        self.assertEqual(self.client.get(reverse("liquidacion:liquidar")).status_code, 405)

    def test_listado_en_pagina_principal(self):
        self.client.post(reverse("liquidacion:liquidar"), VALIDO)
        r = self.client.get(reverse("liquidacion:inicio"))
        self.assertContains(r, "$1.275.225")

    def test_numeracion_consecutiva(self):
        self.client.post(reverse("liquidacion:liquidar"), VALIDO)
        r = self.client.post(reverse("liquidacion:liquidar"), dict(VALIDO, modalidad="CIUDAD"))
        self.assertRedirects(r, reverse("liquidacion:recibo", args=[2]))

    def test_nombre_largo_rechazado(self):
        r = self.client.post(reverse("liquidacion:liquidar"), dict(VALIDO, nombre="A" * 150))
        self.assertContains(r, "no puede superar 100 caracteres", status_code=400)
