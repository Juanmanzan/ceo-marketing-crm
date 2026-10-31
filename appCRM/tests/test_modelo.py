
from django.test import TestCase
from django.core.exceptions import ValidationError

from appCRM.models import Cliente


class TestModeloCliente(TestCase):

    def test_crear_cliente(self):
        cliente = Cliente.objects.create(
            name="Pedro Ramirez",
            email="pedro@test.com",
            status="Prospecto"
        )

        self.assertIsNotNone(cliente.id)
        self.assertEqual(cliente.name, "Pedro Ramirez")

    def test_estado_predeterminado(self):
        cliente = Cliente.objects.create(
            name="Ana Torres",
            email="ana@test.com"
        )

        self.assertEqual(cliente.status, "Prospecto")

    def test_telefono_invalido(self):
        cliente = Cliente(
            name="Luis Gomez",
            email="luis@test.com",
            phone="099ABC1234"
        )

        with self.assertRaises(ValidationError):
            cliente.full_clean()

    def test_estado_invalido(self):
        cliente = Cliente(
            name="Carlos Mena",
            email="carlos@test.com",
            status="Desconocido"
        )

        with self.assertRaises(ValidationError):
            cliente.full_clean()

    def test_email_invalido(self):
        cliente = Cliente(
            name="Maria Perez",
            email="correo-invalido"
        )

        with self.assertRaises(ValidationError):
            cliente.full_clean()

    def test_nombre_obligatorio(self):
        cliente = Cliente(
            name="",
            email="prueba@test.com"
        )

        with self.assertRaises(ValidationError):
            cliente.full_clean()

    def test_representacion_cliente(self):
        cliente = Cliente.objects.create(
            name="Laura Sanchez",
            email="laura@test.com"
        )

        self.assertEqual(str(cliente), "Laura Sanchez")
