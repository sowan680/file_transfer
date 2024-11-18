#!/bin/bash

# Остановка скрипта при ошибке
set -e

# Проверяем, запущен ли скрипт как исполняемый файл
if [ ! -x "$0" ]; then
    echo "Setting execute permission for the script..."
    chmod +x "$0"
fi

# Устанавливаем виртуальное окружение, если его нет
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Активируем виртуальное окружение
source venv/bin/activate

# Устанавливаем зависимости
if [ -f "requirements.txt" ]; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
else
    echo "Error: requirements.txt not found!"
    exit 1
fi

# Запускаем сервер FastAPI с использованием Uvicorn
HOST="0.0.0.0"
PORT="8000"

echo "Starting FastAPI server on http://$HOST:$PORT"
uvicorn server:app --host $HOST --port $PORT --reload
