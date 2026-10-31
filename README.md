# Mini CRM de clientes

Aplicación web desarrollada para la gestión de clientes de CEO Marketing. Permite administrar contactos comerciales mediante una interfaz responsive conectada a una API desarrollada con Django.

## 1. Funcionalidades

- Registro, consulta, actualización y eliminación de clientes.
- Búsqueda de clientes por nombre o empresa.
- Filtrado por estado: prospecto, cliente e inactivo.
- Paginación de resultados.
- Dashboard con indicadores de clientes.
- Validación de formularios y notificaciones.

## 2. Tecnologías utilizadas

| Área | Tecnología |
| :--- | :--- |
| Backend | Python 3.12 y Django 5.2 |
| Frontend | HTML5, CSS3 y JavaScript |
| Base de datos | SQLite |
| Contenedores | Docker y Docker Compose |
| Pruebas | Django TestCase |
| Integración continua | GitHub Actions |

## 3. Arquitectura

El proyecto utiliza una arquitectura que separa la presentación, la lógica de negocio y el acceso a datos.

El frontend utiliza plantillas Django y módulos JavaScript para consumir los endpoints de la API mediante Fetch. El backend gestiona las validaciones y la persistencia mediante el ORM de Django y SQLite.

## 4. Ejecución local

Se requiere tener instalados Docker y Docker Compose.

Crear un archivo `.env` a partir de `.env.example` y configurar las variables de entorno.

Para ejecutar y evaluar el proyecto localmente, se debe configurar DJANGO_DEBUG=1 en el archivo .env. Esta configuración permite utilizar el servidor de desarrollo de Django y cargar los recursos estáticos de la aplicación.

Iniciar los servicios:

```bash
docker compose up -d --build
```

Aplicar las migraciones:

```bash
docker compose exec web python manage.py migrate
```

Acceder a la aplicación:

```text
http://localhost:8000/crm/

```

## 5. Cargar datos de prueba

Opcionalmente, cargar el conjunto de clientes proporcionado con el proyecto:

```bash
docker compose exec web python manage.py loaddata clientes_prueba.json
```
Esta operación permite probar el directorio, la búsqueda, los filtros y los indicadores del dashboard.

## 4. Capturas de pantalla

Se incluyen capturas de las principales funcionalidades del CRM, como el dashboard, la gestión de clientes, los formularios y los filtros.

[Ver capturas de pantalla](docs/capturas/)

## 5. Pruebas automatizadas

Ejecutar las pruebas del proyecto:

```bash
docker compose exec web python manage.py test appCRM.tests
```

## 6. Documentación adicional

La documentación técnica se organiza en los siguientes archivos:

[Guía de instalación](docs/instalacion.md)

[Arquitectura del sistema](docs/arquitectura.md)

[Documentación de la API](docs/api.md)
