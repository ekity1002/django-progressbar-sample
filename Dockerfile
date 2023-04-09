FROM python:3.9.5-slim-buster

WORKDIR /app

RUN apt update && apt install -y \
    curl \
    libgl1-mesa-glx \
    libglib2.0-dev

ENV PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VERSION=1.3.2 \
    PYTHONUNBUFFERED=1

ENV POETRY_HOME=/opt/poetry \
    POETRY_VIRTUALENVS_CREATE=true

ENV PATH=$POETRY_HOME/bin:$PATH

RUN curl -sSL https://install.python-poetry.org/ | python -

COPY . .
RUN poetry install

WORKDIR /app/app
