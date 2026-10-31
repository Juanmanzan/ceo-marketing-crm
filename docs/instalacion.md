# Guía de instalación

## 1. Requisitos previos

Para ejecutar el proyecto se necesita:

- Git.
- Docker y Docker Compose.
- Un puerto 8000 disponible.

No es necesario instalar Python ni SQLite directamente, ya que el proyecto utiliza contenedores Docker.

## 2. Clonar el repositorio

Clonar el proyecto desde GitHub:

```bash
git clone https://github.com/Juanmanzan/ceo-marketing-crm.git
```

Acceder al directorio:

```bash
cd ceo-marketing-crm
```

## 3. Configurar variables de entorno

Crear el archivo `.env` a partir de `.env.example`.

En Windows CMD:

```cmd
copy .env.example .env
```

Generar una clave secreta de Django:

```bash
docker compose run --rm web python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Editar `.env` con los siguientes valores:

```dotenv
DJANGO_SECRET_KEY=CLAVE_GENERADA
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
```

La clave debe ser única y mantenerse privada. El archivo `.env` no debe incluirse en el repositorio.

El valor `DJANGO_DEBUG=True` se utiliza únicamente para la ejecución local.

## 4. Iniciar el proyecto

Construir e iniciar el contenedor:

```bash
docker compose up -d --build
```

Aplicar las migraciones de la base de datos:

```bash
docker compose exec web python manage.py migrate
```

## 5. Cargar datos de prueba

Opcionalmente, cargar el conjunto de clientes proporcionado con el proyecto:

```bash
docker docker compose exec web python manage.py loaddata clientes_prueba.json
```

Esta operación permite probar el directorio, la búsqueda, los filtros y los indicadores del dashboard.

## 6. Acceder a la aplicación

Abrir la siguiente dirección en el navegador:

```text
http://localhost:8000/crm/
```

## 7. Ejecutar las pruebas

Ejecutar las pruebas automatizadas:

```bash
docker compose exec web python manage.py test appCRM.tests
```

Verificar la configuración de Django:

```bash
docker compose exec web python manage.py check
```

## 8. Detener la aplicación

Detener los contenedores:

```bash
docker compose down
```

Para volver a iniciar el CRM:

```bash
docker compose up -d
```
