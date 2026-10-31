import json

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from appCRM.models import Cliente


class TestValidacionNombre(TestCase):

    def setUp(self):
        self.cliente = Cliente.objects.create(
            name="Ana Torres", email="ana@test.com", status="Prospecto"
        )
        self.datos = {
            "name": "Carlos Ramirez", "email": "carlos@test.com",
            "company": "Empresa Uno", "phone": "0991234567", "status": "Cliente"
        }
        self.nombresInvalidos = (
            "12345", "123 456", "Carlos", "Carlos 123", "Carlos2 Ramirez",
            "Carlos @", "Carlos _Ramirez", "   "
        )

    def iniciarAdmin(self):
        usuario = get_user_model().objects.create_superuser(
            username="admin_prueba", email="admin@test.com", password="clave-prueba"
        )
        self.client.force_login(usuario)

    def test_modelo_rechaza_nombres_invalidos(self):
        for nombre in self.nombresInvalidos:
            with self.subTest(nombre=nombre):
                cliente = Cliente(name=nombre, email="nuevo@test.com")
                with self.assertRaises(ValidationError) as error:
                    cliente.full_clean()
                self.assertIn("name", error.exception.message_dict)

    def test_modelo_acepta_nombres_con_tildes_y_apellidos_compuestos(self):
        for nombre in ("María José", "Ana María López", "Jean-Luc Dupont", "María O'Neill", "  Ana   Torres  "):
            with self.subTest(nombre=nombre):
                cliente = Cliente(name=nombre, email="nuevo@test.com")
                cliente.full_clean()

    def test_modelo_conserva_limite_de_nombre(self):
        cliente = Cliente(name="Ana " + "a" * 47, email="nuevo@test.com")
        with self.assertRaises(ValidationError) as error:
            cliente.full_clean()
        self.assertIn("name", error.exception.message_dict)

    def test_post_rechaza_nombres_invalidos(self):
        for nombre in self.nombresInvalidos:
            with self.subTest(nombre=nombre):
                datos = {**self.datos, "name": nombre}
                response = self.client.post(
                    reverse("crear_cliente"), json.dumps(datos), content_type="application/json"
                )
                self.assertEqual(response.status_code, 400)
                self.assertIn("name", response.json()["errors"])
                self.assertEqual(Cliente.objects.count(), 1)

    def test_put_rechaza_nombres_invalidos_sin_cambiar_cliente(self):
        for nombre in self.nombresInvalidos:
            with self.subTest(nombre=nombre):
                datos = {**self.datos, "name": nombre}
                response = self.client.put(
                    reverse("actualizar_cliente", args=[self.cliente.id]),
                    json.dumps(datos), content_type="application/json"
                )
                self.assertEqual(response.status_code, 400)
                self.assertIn("name", response.json()["errors"])
                self.cliente.refresh_from_db()
                self.assertEqual(self.cliente.name, "Ana Torres")
                self.assertEqual(self.cliente.email, "ana@test.com")

    def test_admin_rechaza_nombres_invalidos_al_crear(self):
        self.iniciarAdmin()
        for nombre in self.nombresInvalidos:
            with self.subTest(nombre=nombre):
                response = self.client.post(
                    reverse("admin:appCRM_cliente_add"), {**self.datos, "name": nombre}
                )
                self.assertEqual(response.status_code, 200)
                self.assertIn("name", response.context["adminform"].form.errors)
                self.assertEqual(Cliente.objects.count(), 1)

    def test_admin_rechaza_nombres_invalidos_al_actualizar(self):
        self.iniciarAdmin()
        for nombre in self.nombresInvalidos:
            with self.subTest(nombre=nombre):
                response = self.client.post(
                    reverse("admin:appCRM_cliente_change", args=[self.cliente.id]),
                    {**self.datos, "name": nombre}
                )
                self.assertEqual(response.status_code, 200)
                self.assertIn("name", response.context["adminform"].form.errors)
                self.cliente.refresh_from_db()
                self.assertEqual(self.cliente.name, "Ana Torres")

    def test_admin_crea_y_actualiza_nombre_valido(self):
        self.iniciarAdmin()
        response = self.client.post(reverse("admin:appCRM_cliente_add"), self.datos)
        self.assertEqual(response.status_code, 302)
        cliente = Cliente.objects.get(email=self.datos["email"])

        response = self.client.post(
            reverse("admin:appCRM_cliente_change", args=[cliente.id]),
            {**self.datos, "name": "Carlos Alberto Ramirez"}
        )
        self.assertEqual(response.status_code, 302)
        cliente.refresh_from_db()
        self.assertEqual(cliente.name, "Carlos Alberto Ramirez")
