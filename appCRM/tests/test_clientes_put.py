
import json

from django.test import TestCase
from django.urls import reverse

from appCRM.models import Cliente


class TestActualizarCliente(TestCase):

    def setUp(self):
        # Crear dos clientes para las pruebas
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
            "actualizar_cliente",
            args=[self.cliente1.id]
        )

        self.datos = {
            "name": "Carlos Ramirez Actualizado",
            "company": "Empresa Nueva",
            "email": "carlos.nuevo@test.com",
            "phone": "0999876543",
            "status": "Cliente"
        }

    def enviar_put(self, datos, url=None):
        return self.client.put(
            url or self.url,
            data=json.dumps(datos),
            content_type="application/json"
        )

    def comprobar_error(self, datos, campo):
        response = self.enviar_put(datos)

        self.assertEqual(response.status_code, 400)
        self.assertIn("errors", response.json())
        self.assertIn(campo, response.json()["errors"])

        # Comprobar que los datos originales no cambiaron
        self.cliente1.refresh_from_db()

        self.assertEqual(self.cliente1.name, "Carlos Ramirez")
        self.assertEqual(self.cliente1.email, "carlos@test.com")
        self.assertEqual(Cliente.objects.count(), 2)

    def test_actualizar_cliente_correctamente(self):
        response = self.enviar_put(self.datos)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Cliente.objects.count(), 2)

        self.cliente1.refresh_from_db()

        self.assertEqual(
            self.cliente1.name,
            "Carlos Ramirez Actualizado"
        )
        self.assertEqual(self.cliente1.company, "Empresa Nueva")
        self.assertEqual(self.cliente1.email, "carlos.nuevo@test.com")
        self.assertEqual(self.cliente1.phone, "0999876543")
        self.assertEqual(self.cliente1.status, "Cliente")

    def test_conservar_mismo_id(self):
        response = self.enviar_put(self.datos)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["cliente"]["id"],
            self.cliente1.id
        )
        self.assertEqual(Cliente.objects.count(), 2)

    def test_cliente_inexistente(self):
        url = reverse("actualizar_cliente", args=[99999])

        response = self.enviar_put(self.datos, url=url)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(Cliente.objects.count(), 2)

    def test_nombre_obligatorio(self):
        datos = self.datos.copy()
        datos.pop("name")

        self.comprobar_error(datos, "name")

    def test_email_obligatorio(self):
        datos = self.datos.copy()
        datos.pop("email")

        self.comprobar_error(datos, "email")

    def test_email_invalido(self):
        datos = self.datos.copy()
        datos["email"] = "correo-invalido"

        self.comprobar_error(datos, "email")

    def test_email_duplicado(self):
        datos = self.datos.copy()
        datos["email"] = "maria@test.com"

        self.comprobar_error(datos, "email")

    def test_conservar_email_actual(self):
        datos = self.datos.copy()
        datos["email"] = "carlos@test.com"

        response = self.enviar_put(datos)

        self.assertEqual(response.status_code, 200)

        self.cliente1.refresh_from_db()

        self.assertEqual(self.cliente1.email, "carlos@test.com")
        self.assertEqual(Cliente.objects.count(), 2)

    def test_estado_invalido(self):
        datos = self.datos.copy()
        datos["status"] = "Desconocido"

        self.comprobar_error(datos, "status")

    def test_telefono_invalido(self):
        datos = self.datos.copy()
        datos["phone"] = "099ABC1234"

        self.comprobar_error(datos, "phone")

    def test_json_invalido(self):
        response = self.client.put(
            self.url,
            data='{"name":',
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(Cliente.objects.count(), 2)

    def test_json_no_es_objeto(self):
        response = self.enviar_put([
            {"name": "Carlos"}
        ])

        self.assertEqual(response.status_code, 400)
        self.assertEqual(Cliente.objects.count(), 2)

    def test_metodo_get_no_permitido(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 405)
        self.assertEqual(Cliente.objects.count(), 2)

    def test_fecha_actualizacion(self):
        fecha_anterior = self.cliente1.updated_at

        response = self.enviar_put(self.datos)

        self.assertEqual(response.status_code, 200)

        self.cliente1.refresh_from_db()

        self.assertGreater(
            self.cliente1.updated_at,
            fecha_anterior
        )

    def test_respuesta_contiene_datos_actualizados(self):
        response = self.enviar_put(self.datos)

        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(
            data["mensaje"],
            "Cliente actualizado exitosamente"
        )
        self.assertEqual(
            data["cliente"]["name"],
            "Carlos Ramirez Actualizado"
        )
        self.assertIn("updated_at", data["cliente"])
