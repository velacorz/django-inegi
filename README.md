# django-inegi

Este proyecto permite cargar y gestionar información de estados, municipios, localidades y asentamientos de México usando Django y MySQL. Además, el proyecto está preparado para ejecutarse en contenedores con Docker.

Tecnologías utilizadas

Python 3

Django

MySQL

Docker

Requisitos previos
Antes de iniciar, asegúrate de tener instalado:

Python 3.10+

Docker y Docker Compose

Git

Instalación y configuración

Clona este repositorio:
git clone https://github.com/tuusuario/inegi_project.git

cd inegi_project

Crea un archivo .env en la raíz del proyecto con tus variables de entorno:
MYSQL_DATABASE=inegi_db
MYSQL_USER=inegi_user
MYSQL_PASSWORD=inegi_pass
MYSQL_ROOT_PASSWORD=root_pass

Levanta los servicios con Docker:
docker-compose up --build

Dentro del contenedor, aplica las migraciones:
docker-compose exec web python manage.py migrate

(Opcional) Carga los datos iniciales de INEGI:
docker-compose exec web python manage.py shell < load_inegi.py

Uso

Abre en el navegador: http://localhost:8000

Desde el panel de administración de Django puedes explorar la base de datos:
docker-compose exec web python manage.py createsuperuser

Estructura del proyecto
inegi_project/
│── geo/ # Aplicación principal
│── load_inegi.py # Script para cargar datos de INEGI
│── manage.py
│── Dockerfile
│── docker-compose.yml
│── requirements.txt
│── .env

Comandos útiles

Reconstruir los contenedores:
docker-compose up --build

Acceder al contenedor de Django:
docker-compose exec web bash

Detener los contenedores:
docker-compose down
* MySQL: localhost:3306

## Notas finales

* El código implementa toda la jerarquía (Estado → Municipio → Localidad → Asentamiento).
* Debido a limitaciones actuales de la API del INEGI, solo se obtienen Estados y Municipios.
* El sistema está listo para recibir Localidades y Asentamientos en cuanto la API los proporcione.
* Se optimizó el endpoint con prefetch_related para mejorar el rendimiento.
