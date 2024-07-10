FROM python:3.8-slim

# Установка зависимостей
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Установка переменной окружения для Python в режим отладки
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Создание директории приложения внутри контейнера
RUN mkdir /app

# Установка рабочей директории в контейнере
WORKDIR /app

# Копирование зависимостей в контейнер
COPY requirements.txt /app/

# Установка зависимостей Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Копирование всего содержимого текущей директории в контейнер
COPY . /app/
