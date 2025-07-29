# Используем официальный Python образ
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл зависимостей
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код приложения
COPY . .

# Создаем пользователя для безопасности
RUN adduser --disabled-password --gecos '' appuser && chown -R appuser:appuser /app
USER appuser

# Открываем порт
EXPOSE 5000

# Устанавливаем переменные окружения
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Запускаем приложение
CMD ["python", "app.py"] 