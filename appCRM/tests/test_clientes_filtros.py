from django.test import TestCase
from django.urls import reverse

from appCRM.models import Cliente


class TestClientesFiltros(TestCase):

    def setUp(self):
        self.url = reverse("listar_clientes")
        self.cliente1 = Cliente.objects.create(
            name="Ana Torres",
            company="Marketing Digital",
            email="ana@test.com",
            status="Prospecto"
        )
        self.cliente2 = Cliente.objects.create(
            name="Carlos Perez",
            company="Marketing Digital",
            email="carlos@test.com",
            status="Cliente"
        )
        self.cliente3 = Cliente.objects.create(
            name="Ana Lopez",
            company="Empresa Tres",
            email="ana.lopez@test.com",
            status="Inactivo"
        )

    def test_buscar_por_nombre(self):
        response = self.client.get(self.url, {"buscar": "Ana Torres"})

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual([cliente["id"] for cliente in data["clientes"]], [self.cliente1.id])
        self.assertEqual(data["totalClientes"], 3)
        self.assertEqual(data["totalFiltrados"], 1)

    def test_buscar_por_empresa(self):
        response = self.client.get(self.url, {"buscar": "Marketing Digital"})

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(
            [cliente["id"] for cliente in data["clientes"]],
            [self.cliente1.id, self.cliente2.id]
        )
        self.assertEqual(data["totalClientes"], 3)
        self.assertEqual(data["totalFiltrados"], 2)

    def test_busqueda_parcial_sin_distinguir_mayusculas(self):
        for buscar, ids in (
            ("tOrR", [self.cliente1.id]),
            ("mArKeT", [self.cliente1.id, self.cliente2.id])
        ):
            with self.subTest(buscar=buscar):
                response = self.client.get(self.url, {"buscar": buscar})

                self.assertEqual(response.status_code, 200)
                self.assertEqual(
                    [cliente["id"] for cliente in response.json()["clientes"]], ids
                )

    def test_busqueda_sin_resultados(self):
        response = self.client.get(self.url, {"buscar": "Sin coincidencias"})

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["clientes"], [])
        self.assertEqual(data["totalClientes"], 3)
        self.assertEqual(data["totalFiltrados"], 0)
        self.assertEqual(data["paginacion"], {
            "existeOtraPagina": False, "cursor_next": None
        })

    def test_filtro_por_cada_estado(self):
        for estado, cliente in (
            ("Prospecto", self.cliente1),
            ("Cliente", self.cliente2),
            ("Inactivo", self.cliente3)
        ):
            with self.subTest(estado=estado):
                response = self.client.get(self.url, {"estado": estado})

                self.assertEqual(response.status_code, 200)
                data = response.json()
                self.assertEqual([dato["id"] for dato in data["clientes"]], [cliente.id])
                self.assertEqual(data["totalClientes"], 3)
                self.assertEqual(data["totalFiltrados"], 1)

    def test_busqueda_combinada_con_estado(self):
        for buscar, estado, cliente in (
            ("ANA", "Inactivo", self.cliente3),
            ("MARKETING", "Cliente", self.cliente2)
        ):
            with self.subTest(buscar=buscar, estado=estado):
                response = self.client.get(self.url, {"buscar": buscar, "estado": estado})

                self.assertEqual(response.status_code, 200)
                data = response.json()
                self.assertEqual([dato["id"] for dato in data["clientes"]], [cliente.id])
                self.assertEqual(data["totalFiltrados"], 1)
                self.assertEqual(data["totalClientes"], 3)

    def test_estado_invalido(self):
        for estado in ("Desconocido", "cliente", "", " Cliente "):
            with self.subTest(estado=estado):
                response = self.client.get(self.url, {"estado": estado})

                self.assertEqual(response.status_code, 400)
                self.assertIn("error", response.json())

    def test_cursor_invalido(self):
        for cursor in ("abc", "-1", "1.5", "", " ", "9223372036854775808", "9" * 5000):
            with self.subTest(cursor=cursor[:30]):
                response = self.client.get(self.url, {"cursor": cursor})

                self.assertEqual(response.status_code, 400)
                self.assertIn("error", response.json())

    def test_cursor_cero(self):
        response = self.client.get(self.url, {"cursor": "0"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["clientes"]), 3)

    def test_paginacion_con_filtros(self):
        ids = [self.cliente2.id]
        for i in range(11):
            cliente = Cliente.objects.create(
                name=f"Contacto {i}",
                company="Marketing Digital",
                email=f"contacto{i}@test.com",
                status="Cliente"
            )
            ids.append(cliente.id)

        parametros = {"buscar": "MARKET", "estado": "Cliente"}
        response = self.client.get(self.url, parametros)

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual([cliente["id"] for cliente in data["clientes"]], ids[:10])
        self.assertEqual(data["totalClientes"], 14)
        self.assertEqual(data["totalFiltrados"], 12)
        self.assertEqual(data["paginacion"], {
            "existeOtraPagina": True, "cursor_next": ids[9]
        })

        parametros["cursor"] = data["paginacion"]["cursor_next"]
        response = self.client.get(self.url, parametros)

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual([cliente["id"] for cliente in data["clientes"]], ids[10:])
        self.assertEqual(data["totalClientes"], 14)
        self.assertEqual(data["totalFiltrados"], 12)
        self.assertEqual(data["paginacion"], {
            "existeOtraPagina": False, "cursor_next": None
        })

    def test_pagina_con_diez_resultados_no_tiene_siguiente(self):
        for i in range(9):
            Cliente.objects.create(
                name=f"Contacto {i}", email=f"contacto{i}@test.com", status="Cliente"
            )

        response = self.client.get(self.url, {"estado": "Cliente"})

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data["clientes"]), 10)
        self.assertEqual(data["totalFiltrados"], 10)
        self.assertEqual(data["paginacion"], {
            "existeOtraPagina": False, "cursor_next": None
        })

    def test_cursor_sin_resultados_conserva_totales(self):
        response = self.client.get(self.url, {
            "estado": "Cliente", "cursor": self.cliente3.id
        })

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["clientes"], [])
        self.assertEqual(data["totalClientes"], 3)
        self.assertEqual(data["totalFiltrados"], 1)
        self.assertEqual(data["paginacion"], {
            "existeOtraPagina": False, "cursor_next": None
        })

    def test_listado_sin_parametros(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["totalClientes"], 3)
        self.assertEqual(data["totalFiltrados"], 3)
        self.assertEqual(
            [cliente["id"] for cliente in data["clientes"]],
            [self.cliente1.id, self.cliente2.id, self.cliente3.id]
        )
        self.assertEqual(set(data["clientes"][0]), {
            "id", "name", "company", "email", "phone", "status", "created_at"
        })

    def test_busqueda_vacia(self):
        for buscar in ("", "   "):
            with self.subTest(buscar=buscar):
                response = self.client.get(self.url, {"buscar": buscar})

                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.json()["totalFiltrados"], 3)

    def test_listado_vacio(self):
        Cliente.objects.all().delete()

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "clientes": [], "totalClientes": 0, "totalFiltrados": 0,
            "paginacion": {"existeOtraPagina": False, "cursor_next": None}
        })

    def test_consultas_del_listado(self):
        with self.assertNumQueries(2):
            response = self.client.get(self.url, {"buscar": "Marketing", "estado": "Cliente"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["totalFiltrados"], 1)

    def test_metodos_no_permitidos(self):
        for metodo in ("post", "put", "patch", "delete", "head", "options"):
            with self.subTest(metodo=metodo):
                response = getattr(self.client, metodo)(self.url)

                self.assertEqual(response.status_code, 405)
                self.assertEqual(response.headers["Allow"], "GET")
