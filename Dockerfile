# Use Python 3.12 slim image
FROM python:3.12-slim

# Install system dependencies (poppler-utils is required for pdf2image)
RUN apt-get update && apt-get install -y \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Set default port
ENV PORT 10000
EXPOSE $PORT

# Gunicorn configuration:
# --timeout: Increase to 120s for long PDF processing
# --workers: Set to 1 to save memory on Render Free tier
# --threads: Use threads instead of multiple workers for better memory efficiency
CMD gunicorn --bind 0.0.0.0:$PORT --timeout 120 --workers 1 --threads 4 app:app
