FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код приложения
COPY bot/ ./bot/

# Создаем папку для базы данных
RUN mkdir -p data

# Запускаем бота
CMD ["python", "-m", "bot.app"]

