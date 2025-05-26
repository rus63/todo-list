FROM python:3.12.6-slim

RUN apt-get update -qq \
    && DEBIAN_FRONTEND=noninteractive apt-get install -yq --no-install-recommends \
        apt-transport-https \
        build-essential \
        ca-certificates \
        curl \
        git \
        gnupg \
        jq \
        less \
        libcairo2 \
        libffi-dev \
        libgdk-pixbuf2.0-0 \
        libpango-1.0-0 \
        libpangocairo-1.0-0 \
        libpcre3 \
        libpcre3-dev \
        libxml2-dev \
        libxslt-dev \
        openssh-client \
        shared-mime-info \
        telnet \
        unzip \
        vim \
        wget \
    && apt-get clean \
    && rm -rf /var/cache/apt/archives/* \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* \
    && truncate -s 0 /var/log/*log

ENV PATH="/root/.local/bin:$PATH"

RUN curl -sSL https://install.python-poetry.org | python3 - --version 1.8.3 \
    && poetry config virtualenvs.create false \
#    && poetry config http-basic.dbp $READ_PACKAGE_TOKEN NOPASS \
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