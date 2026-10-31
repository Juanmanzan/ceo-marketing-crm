
from django.test import TestCase
from django.urls import reverse

from appCRM.models import Cliente


class TestEliminarCliente(TestCase):

    def setUp(self):
        # Clientes utilizados para las pruebas
        self.cliente1 = Cliente.objects.create(
            name="Carlos Ramirez",
            company="Empresa Uno",
            email="carlos@test.com",
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

        self.url = reverse(
            "eliminar_cliente",
            args=[self.cliente1.id]
        )

    def test_eliminar_cliente_correctamente(self):
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Cliente.objects.count(), 1)

        self.assertFalse(
            Cliente.objects.filter(id=self.cliente1.id).exists()
        )

    def test_respuesta_eliminacion(self):
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(
            data["mensaje"],
            "Cliente eliminado exitosamente"
        )
        self.assertEqual(data["id"], self.cliente1.id)
        self.assertEqual(data["name"], "Carlos Ramirez")

    def test_cliente_inexistente(self):
        url = reverse("eliminar_cliente", args=[99999])

        response = self.client.delete(url)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json()["error"],
            "Cliente no encontrado"
        )
        self.assertEqual(Cliente.objects.count(), 2)

    def test_no_eliminar_otros_clientes(self):
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, 200)

        self.assertTrue(
            Cliente.objects.filter(id=self.cliente2.id).exists()
        )

        self.assertEqual(Cliente.objects.count(), 1)

    def test_eliminar_cliente_dos_veces(self):
        # Primera eliminación
        response1 = self.client.delete(self.url)

        self.assertEqual(response1.status_code, 200)

        # Segunda eliminación
        response2 = self.client.delete(self.url)

        self.assertEqual(response2.status_code, 404)
        self.assertEqual(Cliente.objects.count(), 1)

    def test_metodo_get_no_permitido(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 405)
        self.assertEqual(Cliente.objects.count(), 2)

    def test_cliente_no_disponible_despues_eliminar(self):
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, 200)

        # Consultar el cliente mediante el endpoint GET
        url_detalle = reverse(
            "detalle_cliente",
            args=[self.cliente1.id]
        )

        response_get = self.client.get(url_detalle)

        self.assertEqual(response_get.status_code, 404)
