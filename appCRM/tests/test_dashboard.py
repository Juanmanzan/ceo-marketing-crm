from django.test import TestCase
from django.urls import reverse

from appCRM.models import Cliente


class TestDashboard(TestCase):

    def setUp(self):
        self.url = reverse("resumen_clientes")
        for i, estado in enumerate(("Prospecto", "Prospecto", "Prospecto", "Cliente", "Cliente", "Inactivo")):
            Cliente.objects.create(
                name=f"Contacto {i}",
                email=f"contacto{i}@test.com",
                status=estado
            )

        self.resumen = {
            "totalClientes": 6,
            "prospectos": 3,
            "clientesActivos": 2,
            "inactivos": 1
        }

    def test_kpi_por_estado(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.json(), self.resumen)

    def test_kpi_base_vacia(self):
        Cliente.objects.all().delete()

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "totalClientes": 0,
            "prospectos": 0,
            "clientesActivos": 0,
            "inactivos": 0
        })

    def test_kpi_sin_clientes_de_un_estado(self):
        Cliente.objects.filter(status="Inactivo").delete()

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "totalClientes": 5,
            "prospectos": 3,
            "clientesActivos": 2,
            "inactivos": 0
        })

    def test_kpi_ignoran_filtros_y_cursor(self):
        response = self.client.get(self.url, {
            "buscar": "Sin coincidencias", "estado": "Cliente", "cursor": 99999
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), self.resumen)

    def test_kpi_incluyen_clientes_fuera_de_la_primera_pagina(self):
        for i in range(12):
            Cliente.objects.create(
                name=f"Adicional {i}", email=f"adicional{i}@test.com", status="Cliente"
            )

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "totalClientes": 18,
            "prospectos": 3,
            "clientesActivos": 14,
            "inactivos": 1
        })

    def test_kpi_utilizan_una_consulta(self):
        with self.assertNumQueries(1):
            response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), self.resumen)

    def test_metodos_no_permitidos(self):
        for metodo in ("post", "put", "patch", "delete", "head", "options"):
            with self.subTest(metodo=metodo):
                response = getattr(self.client, metodo)(self.url)

                self.assertEqual(response.status_code, 405)
                self.assertEqual(response.headers["Allow"], "GET")
