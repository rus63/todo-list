FROM python:3.12.6-slim

RUN apt-get update && apt-get install -y curl

ENV PATH="/root/.local/bin:$PATH"

RUN curl -sSL https://install.python-poetry.org | python3 - --version 1.8.3 \
    && poetry config virtualenvs.create false \
    && mkdir -p /app \


RUN poetry config virtualenvs.create false

RUN mkdir -p /app
WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN poetry install  --no-interaction --no-ansi

ADD . /app
ENV DJANGO_SETTINGS_MODULE="todo_list.settings"

EXPOSE 8000

CMD python manage.py runserver 0.0.0.0:8000