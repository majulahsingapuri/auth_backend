# Backend

## Prerequisites

* Python 3.9+
* Poetry (<https://python-poetry.org/docs/>)
* Docker

## Setup

1. Install dependencies with Poetry. This will also create a virtual environment at `.venv` if it does not exist yet.

   ```bash
   poetry install
   ```

2. Activate the virtual environment. The command is different depending on your OS and shell.
   Alternatively, `poetry shell` may work, but it might not launch the correct shell.

3. Copy the `template.env` file to `.env`, which will be used to configure the application.

   ```bash
   cp template.env .env
   ```

4. Create a volume to persist the database between container restarts:

   ```bash
   docker volume create auth_db
   ```

5. Start the database container:

   ```bash
   docker run -d -v auth_db:/var/lib/postgresql/data -e POSTGRES_USER=auth -e POSTGRES_PASSWORD=password -e POSTGRES_DB=auth -p 5432:5432 --name auth_db postgres
   ```

6. Run database migrations.

   ```bash
   python manage.py migrate
   ```

7. Set up pre-commit hooks.

   ```bash
   pre-commit install
   ```

8. Run the test suite with coverage

   ```bash
   pytest --cov
   ```

9. Create a local superuser.

   ```bash
   python manage.py createsuperuser
   ```

10. Start the development server. This will listen on localhost:8000.

      ```bash
      python manage.py runserver
      ```

11. Start the frontend server. This will listen on localhost:3000
