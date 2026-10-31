
from django.test import TestCase
from django.urls import reverse

from appCRM.models import Cliente


class TestClientesGET(TestCase):

    def setUp(self):
        self.cliente1 = Cliente.objects.create(
            name="Juan Perez",
            company="Empresa Uno",
            email="juan@test.com",
            phone="0991234567",
            status="Prospecto"
        )

        self.cliente2 = Cliente.objects.create(
            name="Maria Lopez",
            company="Empresa Dos",
            email="maria@test.com",
            phone="0987654321",
            status="Cliente"
        )

    def test_listar_clientes(self):
        # Consultar el endpoint de listado
        response = self.client.get(reverse("listar_clientes"))

        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(data["totalClientes"], 2)
        self.assertEqual(len(data["clientes"]), 2)

    def test_listado_vacio(self):
        # Eliminar los clientes de prueba
        Cliente.objects.all().delete()

        response = self.client.get(reverse("listar_clientes"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["totalClientes"], 0)
        self.assertEqual(response.json()["clientes"], [])

    def test_paginacion_clientes(self):
        # Crear 10 clientes adicionales para superar el limite
        for i in range(10):
            Cliente.objects.create(
                name=f"Cliente {i}",
                email=f"cliente{i}@test.com",
                status="Prospecto"
            )

        response = self.client.get(reverse("listar_clientes"))

        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(data["totalClientes"], 12)
        self.assertEqual(len(data["clientes"]), 10)
        self.assertTrue(data["paginacion"]["existeOtraPagina"])
        self.assertIsNotNone(data["paginacion"]["cursor_next"])

        # Consultar la siguiente pagina
        cursor = data["paginacion"]["cursor_next"]

        response2 = self.client.get(
            reverse("listar_clientes"),
            {"cursor": cursor}
        )

        self.assertEqual(response2.status_code, 200)
        self.assertEqual(len(response2.json()["clientes"]), 2)
        self.assertFalse(
            response2.json()["paginacion"]["existeOtraPagina"]
        )

    def test_cursor_invalido(self):
        response = self.client.get(
            reverse("listar_clientes"),
            {"cursor": "abc"}
        )

        self.assertEqual(response.status_code, 400)

    def test_ver_cliente_existente(self):
        response = self.client.get(
            reverse("detalle_cliente", args=[self.cliente1.id])
        )

        self.assertEqual(response.status_code, 200)

        data = response.json()["cliente"]

        self.assertEqual(data["id"], self.cliente1.id)
        self.assertEqual(data["name"], "Juan Perez")
        self.assertEqual(data["email"], "juan@test.com")

    def test_ver_cliente_inexistente(self):
        response = self.client.get(
            reverse("detalle_cliente", args=[99999])
        )

        self.assertEqual(response.status_code, 404)

    def test_metodo_no_permitido(self):
        response = self.client.post(
            reverse("detalle_cliente", args=[self.cliente1.id])
        )

        self.assertEqual(response.status_code, 405)
