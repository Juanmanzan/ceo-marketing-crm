# Mini CRM de clientes

Aplicación web desarrollada para la gestión de clientes de CEO Marketing. Permite administrar contactos comerciales mediante una interfaz responsive conectada a una API desarrollada con Django.

## 1. Funcionalidades

- Registro, consulta, actualización y eliminación de clientes.
- Búsqueda de clientes por nombre o empresa.
- Filtrado por estado: prospecto, cliente e inactivo.
- Paginación de resultados.
- Dashboard con indicadores de clientes.
- Validación de formularios y notificaciones.
- Administración de clientes mediante Django Admin.

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

## 4. Instalación y ejecución local

### 4.1. Requisitos previos

Para ejecutar el proyecto se necesita:

- Git.
- Docker con Docker Compose.
- Puerto 8000 disponible.

No es necesario instalar Python ni SQLite directamente, ya que el proyecto se ejecuta mediante Docker.

### 4.2. Clonar el repositorio

Clonar el proyecto desde GitHub:

```bash
git clone https://github.com/Juanmanzan/ceo-marketing-crm.git
```

Acceder al directorio del proyecto:

```bash
cd ceo-marketing-crm
```

Todos los comandos siguientes deben ejecutarse desde este directorio.

### 4.3. Configurar las variables de entorno

Crear el archivo `.env` a partir de `.env.example`.

En Windows CMD:

```cmd
copy .env.example .env
```

En Linux o macOS:

```bash
cp .env.example .env
```

Generar una clave secreta de Django:

```bash
docker compose run --rm web python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copiar la clave generada y configurar el archivo `.env` con estos valores:

```dotenv
DJANGO_DEBUG=1
DJANGO_SECRET_KEY=CLAVE_GENERADA
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
```

Reemplazar `CLAVE_GENERADA` con el valor obtenido anteriormente.

**Importante:** este proyecto utiliza `DJANGO_DEBUG=1` para activar el modo de desarrollo. No se debe utilizar `DJANGO_DEBUG=True`, ya que la configuración actual de Django reconoce únicamente el valor `1`.

La clave secreta debe mantenerse privada y el archivo `.env` no debe subirse al repositorio.

Esta configuración está destinada a la ejecución local. Para producción se requiere `DJANGO_DEBUG=0`, un servidor de aplicación apropiado y una configuración adecuada de archivos estáticos y seguridad.

### 4.4. Construir e iniciar el proyecto

Construir la imagen e iniciar el servicio:

```bash
docker compose up -d --build
```

Comprobar que el contenedor se encuentre en ejecución:

```bash
docker compose ps
```

### 4.5. Aplicar las migraciones

Inicializar la base de datos mediante las migraciones de Django:

```bash
docker compose exec web python manage.py migrate
```

Este paso crea las tablas necesarias para el funcionamiento del sistema.

### 4.6. Cargar los datos de ejemplo

Para evaluar las funcionalidades del CRM con clientes precargados, ejecutar:

```bash
docker compose exec web python manage.py loaddata clientes_prueba
```

El proyecto incluye un conjunto de datos de ejemplo que permite probar el directorio de clientes, la búsqueda, los filtros, la paginación y los indicadores del dashboard.

**Se recomienda ejecutar esta carga en una base de datos recién inicializada.** No es necesario volver a cargarla cada vez que se inicia el proyecto, y hacerlo sobre una base con datos existentes podría actualizar o generar conflictos con registros que utilizan los mismos identificadores.

La carga es opcional si se desea registrar clientes manualmente, pero se recomienda para una evaluación completa de la interfaz.

### 4.7. Crear un superusuario

Para acceder al panel administrativo de Django, crear un superusuario mediante:

```bash
docker compose exec web python manage.py createsuperuser
```

Ingresar el nombre de usuario, correo electrónico y contraseña solicitados en la terminal.

Estas credenciales permitirán acceder al panel administrativo.

### 4.8. Acceder a la aplicación

Una vez completada la configuración, abrir las siguientes direcciones en el navegador.

**CRM de clientes:**

http://localhost:8000/crm/

**Panel administrativo de Django:**

http://localhost:8000/admin/

En el CRM se pueden consultar y administrar clientes mediante la interfaz principal.

En Django Admin se pueden gestionar los clientes utilizando las credenciales del superusuario creado anteriormente.

## 5. Pruebas automatizadas

El proyecto incluye pruebas automatizadas para verificar el funcionamiento del modelo, las validaciones, los endpoints y los indicadores.

### 5.1. Ejecutar las pruebas

Con el contenedor en ejecución:

```bash
docker compose exec web python manage.py test appCRM.tests
```

Django crea una base de datos temporal para las pruebas, por lo que **no es necesario cargar previamente `clientes_prueba` para ejecutar este comando**.

Los datos de ejemplo de la sección 4.6 se utilizan para evaluar manualmente la aplicación con información precargada.

### 5.2. Verificar la configuración

Ejecutar la comprobación de configuración de Django:

```bash
docker compose exec web python manage.py check
```

Ambos comandos permiten comprobar el funcionamiento del proyecto antes de su evaluación o entrega.

## 6. Capturas de pantalla

Se incluyen capturas de las principales funcionalidades del CRM, como el dashboard, el directorio de clientes, los formularios y los filtros.

[Ver capturas de pantalla](docs/capturas/)

## 7. Detener y reiniciar el proyecto

Para detener los contenedores:

```bash
docker compose down
```

Para volver a iniciar el proyecto sin reconstruir la imagen:

```bash
docker compose up -d
```

Este procedimiento no elimina la base de datos existente.

## 8. Documentación adicional

La documentación técnica se encuentra disponible en los siguientes archivos:

- [Arquitectura del sistema](docs/arquitectura.md)
- [Documentación de la API](docs/api.md)