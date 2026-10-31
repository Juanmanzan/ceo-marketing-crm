# Documentación de la API

## 1. Descripción general

La API del Mini CRM permite gestionar clientes mediante solicitudes HTTP y respuestas en formato JSON.

La URL base es:

```text
http://localhost:8000/api/
```

## 2. Endpoints disponibles

| Método | Endpoint | Descripción |
| :--- | :--- | :--- |
| GET | `/clientes/` | Listar clientes |
| GET | `/clientes/{id}/` | Consultar un cliente |
| POST | `/clientes/crear/` | Registrar un cliente |
| PUT | `/clientes/{id}/actualizar/` | Actualizar un cliente |
| DELETE | `/clientes/{id}/eliminar/` | Eliminar un cliente |
| GET | `/clientes/resumen/` | Obtener indicadores del dashboard |

## 3. Búsqueda, filtros y paginación

El endpoint de listado admite parámetros opcionales.

| Parámetro | Descripción |
| :--- | :--- |
| `buscar` | Buscar por nombre o empresa |
| `estado` | Filtrar por Prospecto, Cliente o Inactivo |
| `cursor` | Continuar la paginación desde un identificador |

Ejemplo:

```http
GET /api/clientes/?buscar=marketing&estado=Cliente
```

El listado devuelve hasta 10 registros por solicitud, junto con el número total de clientes, el total filtrado y la información de paginación.

```json
{
  "clientes": [],
  "totalClientes": 50,
  "totalFiltrados": 0,
  "paginacion": {
    "existeOtraPagina": false,
    "cursor_next": null
  }
}
```

Los valores mostrados son ilustrativos.

## 4. Registro y actualización

Las operaciones POST y PUT reciben un objeto JSON con los datos del cliente.

```json
{
  "name": "Ana Torres",
  "company": "Empresa Demo",
  "email": "ana@example.com",
  "phone": "0991234567",
  "status": "Prospecto"
}
```

Los campos `name` y `email` son obligatorios. `company` y `phone` son opcionales.

El estado admite los valores `Prospecto`, `Cliente` e `Inactivo`. Al crear un cliente, se utiliza `Prospecto` si no se proporciona un estado.

Para actualizar un cliente se envía el formulario completo, incluidos los campos obligatorios.

## 5. Indicadores del dashboard

El endpoint `/api/clientes/resumen/` devuelve los indicadores generales.

```json
{
  "totalClientes": 50,
  "prospectos": 20,
  "clientesActivos": 25,
  "inactivos": 5
}
```

Los valores se calculan a partir de los registros almacenados en SQLite.

## 6. Códigos de respuesta

| Código | Significado |
| :--- | :--- |
| 200 | Solicitud procesada correctamente |
| 201 | Cliente creado |
| 400 | Datos o parámetros inválidos |
| 403 | Solicitud rechazada por protección CSRF |
| 404 | Cliente no encontrado |
| 405 | Método HTTP no permitido |
| 409 | Conflicto de datos |

## 7. Seguridad

Las operaciones POST, PUT y DELETE requieren un token CSRF válido.

Desde el frontend, el token se envía mediante la cabecera `X-CSRFToken`, junto con las cookies correspondientes a la sesión del navegador.

La API utiliza las validaciones de Django para comprobar los campos y evitar registros inválidos.
