FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["celery", "-A", "backend.celery:app", "beat", "-l", "info"]
