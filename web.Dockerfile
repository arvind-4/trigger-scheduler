FROM python:3.11-slim as builder

RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN python -m venv /opt/venv
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput
RUN python manage.py migrate --noinput

CMD ["/opt/venv/bin/gunicorn", "--bind", "0.0.0.0:8000", "-w", "2", "-k", "uvicorn.workers.UvicornWorker", "backend.asgi:application"]
