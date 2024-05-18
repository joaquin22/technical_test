# Prueba Tecnica Django

Este es un proyecto Django configurado para ejecutarse con Docker.

## Requisitos previos

Asegúrate de tener instalados lo siguiente antes de continuar:

- Docker: [Instalación de Docker](https://docs.docker.com/get-docker/)
- Docker Compose: [Instalación de Docker Compose](https://docs.docker.com/compose/install/)

Si deseas ejecutar el proyecto en tu máquina local, asegúrate de tener instalados lo siguiente:

- Python 3.11
- Poetry [Instalación de Poetry](https://python-poetry.org/docs/#installation)

## Configuración del entorno de desarrollo

1. **Clonar el repositorio:**

   ```bash
    git clone https://github.com/joaquin22/technical_test.git
    cd technical_test
    ```

2. **Construir y levantar el proyecto:**
    - **Usando Docker:**

      ```bash
        docker-compose up -d --build
        docker-compose exec web poetry run python manage.py createsuperuser
        ```
    - **Usando Poetry:**

      ```bash
        python -m venv venv
        source venv/bin/activate
        poetry install
        poetry run python manage.py migrate
        poetry run python manage.py createsuperuser
        poetry run python manage.py runserver
        ```

  Para crear un API key, se debe de hacer desde el panel de administración de Django. http://localhost:8000/admin/

El proyecto estará disponible en http://localhost:8000.


## Ejecución de pruebas

Para ejecutar las pruebas, se esta usando [pytest](https://docs.pytest.org/en/7.2.x/) y [pytest-django](https://pytest-django.readthedocs.io/en/latest/).

Para ejecutar las pruebas, debes de ejecutar el siguiente comando:

```bash
pytest
```