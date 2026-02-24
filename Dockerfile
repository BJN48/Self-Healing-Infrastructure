FROM python:3.11-slim

WORKDIR /app

COPY webhook.py .
COPY restart.yml .

RUN apt-get update && apt-get install -y ansible docker.io

EXPOSE 5001

CMD ["python", "webhook.py"]
