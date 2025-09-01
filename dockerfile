FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

# Pequeño retraso para esperar a que MySQL quede healthy en entornos lentos
CMD ["sh", "-c", "sleep 5 && gunicorn --bind 0.0.0.0:5000 --workers 1 --timeout 120 run:app"]
