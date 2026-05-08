FROM python:3.13-slim

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y \
    libxcb1 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libglib2.0-0 \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "app.py"]
