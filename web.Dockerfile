FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

RUN chmod +x /app/docker-entrypoint.sh 

ENTRYPOINT ["/app/docker-entrypoint.sh"]
