# Этап 1: сборка зависимостей
FROM python:3.13-slim AS builder

# Установим системные зависимости для сборки
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    gcc \
    libffi-dev \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Установка poetry
RUN pip install --no-cache-dir poetry

# Установка зависимостей проекта
WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# Этап 2: финальный образ
FROM python:3.13-slim

# Установим только нужные системные библиотеки для работы (без компиляции)
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Копируем только зависимости из билдера
COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Копируем код проекта
COPY . .

ENV PORT=8000
EXPOSE $PORT

CMD ["sh", "-c", "alembic upgrade head && gunicorn src.main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT"]
