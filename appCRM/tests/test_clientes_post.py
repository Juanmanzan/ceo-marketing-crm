
import json

from django.test import TestCase
from django.urls import reverse

from appCRM.models import Cliente


class TestCrearCliente(TestCase):

    def setUp(self):
        # Ruta del endpoint POST
        self.url = reverse("crear_cliente")

        # Datos válidos para las pruebas
        self.datos = {
            "name": "Carlos Ramirez",
            "company": "Innovacion Digital",
            "email": "carlos@test.com",
            "phone": "0991234567",
            "status": "Prospecto"
        }

    def enviar_post(self, datos):
        return self.client.post(
            self.url,
            data=json.dumps(datos),
            content_type="application/json"
        )

    def test_crear_cliente_correctamente(self):
        response = self.enviar_post(self.datos)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Cliente.objects.count(), 1)

        cliente = Cliente.objects.get(email="carlos@test.com")

        self.assertEqual(cliente.name, "Carlos Ramirez")
        self.assertEqual(cliente.company, "Innovacion Digital")
        self.assertEqual(cliente.status, "Prospecto")

        self.assertEqual(
            response.json()["cliente"]["id"],
            cliente.id
        )

    def test_crear_cliente_solo_campos_obligatorios(self):
        datos = {
            "name": "Maria Lopez",
            "email": "maria@test.com"
        }

        response = self.enviar_post(datos)

        print("STATUS:", response.status_code, flush=True)
        print("ERRORES:", response.json(), flush=True)

        self.assertEqual(response.status_code, 201)


        self.assertEqual(response.status_code, 201)
        self.assertEqual(Cliente.objects.count(), 1)

        cliente = Cliente.objects.get(email="maria@test.com")

        self.assertEqual(cliente.status, "Prospecto")
        self.assertEqual(cliente.company, "")
        self.assertEqual(cliente.phone, "")

        

    def test_nombre_obligatorio(self):
        datos = self.datos.copy()
        datos.pop("name")

        response = self.enviar_post(datos)

        self.assertEqual(response.status_code, 400)
        self.assertIn("name", response.json()["errors"])
        self.assertEqual(Cliente.objects.count(), 0)

    def test_email_obligatorio(self):
        datos = self.datos.copy()
        datos.pop("email")

        response = self.enviar_post(datos)

        self.assertEqual(response.status_code, 400)
        self.assertIn("email", response.json()["errors"])
        self.assertEqual(Cliente.objects.count(), 0)

    def test_email_invalido(self):
        datos = self.datos.copy()
        datos["email"] = "correo-invalido"

        response = self.enviar_post(datos)

        self.assertEqual(response.status_code, 400)
        self.assertIn("email", response.json()["errors"])
        self.assertEqual(Cliente.objects.count(), 0)

    def test_email_duplicado(self):
        Cliente.objects.create(
            name="Cliente existente",
            email="carlos@test.com"
        )

        response = self.enviar_post(self.datos)

        self.assertEqual(response.status_code, 400)
        self.assertIn("email", response.json()["errors"])
        self.assertEqual(Cliente.objects.count(), 1)

    def test_estado_invalido(self):
        datos = self.datos.copy()
        datos["status"] = "Desconocido"

        response = self.enviar_post(datos)

        self.assertEqual(response.status_code, 400)
        self.assertIn("status", response.json()["errors"])
        self.assertEqual(Cliente.objects.count(), 0)

    def test_telefono_invalido(self):
        datos = self.datos.copy()
        datos["phone"] = "099ABC1234"

        response = self.enviar_post(datos)

        self.assertEqual(response.status_code, 400)
        self.assertIn("phone", response.json()["errors"])
        self.assertEqual(Cliente.objects.count(), 0)

    def test_json_invalido(self):
        response = self.client.post(
            self.url,
            data='{"name":',
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(Cliente.objects.count(), 0)

    def test_json_no_es_objeto(self):
        response = self.enviar_post([
            {"name": "Carlos Ramirez"}
        ])

        self.assertEqual(response.status_code, 400)
        self.assertEqual(Cliente.objects.count(), 0)

    def test_metodo_get_no_permitido(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 405)
        self.assertEqual(Cliente.objects.count(), 0)
