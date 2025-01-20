#!/bin/bash

# Ожидание запуска базы данных. Контейнер с базой данных не должен развернуться позже срабатывания данной команды
echo "Waiting for database to be ready..."
while ! nc -z ${POSTGRES_HOST} ${POSTGRES_PORT}; do
  sleep 3
done
echo "Database is ready."

# Применение миграций
echo "Applying database migrations..."
alembic upgrade head

# Запуск приложения
echo "Starting application..."
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000