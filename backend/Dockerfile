FROM python:3.13-slim

WORKDIR /app

# Copy the entire project root so models/ is available alongside backend/
COPY . .

RUN apt-get update && apt-get install -y \
    libxcb1 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libglib2.0-0 \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r backend/requirements.txt

# Run app.py from the backend directory so relative paths resolve correctly
WORKDIR /app/backend

CMD ["python", "app.py"]
