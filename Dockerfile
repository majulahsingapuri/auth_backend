FROM python:3.10-slim-buster

SHELL ["/bin/bash", "-c"] 

# Install Poetry
RUN pip install poetry

# Copy files
WORKDIR /app
COPY . /app
RUN mv prod.env .env

# Install Dependencies
RUN poetry export --without-hashes --format=requirements.txt > requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

EXPOSE 8000

CMD [ "gunicorn", "auth.wsgi:application", "--bind", "0.0.0.0:8000" ]