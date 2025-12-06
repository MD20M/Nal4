FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && \
    apt-get install -y fonts-dejavu-core && \
    rm -rf /var/lib/apt/lists/*

COPY . .

ENV PORT=5000

EXPOSE 5000

CMD ["python", "app.py"]