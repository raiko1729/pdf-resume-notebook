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

# Expose port (Cloud Run uses PORT environment variable, defaults to 8080 or as configured)
EXPOSE 8080

# ポート番号を環境変数 $PORT から取得して起動するように変更
CMD gunicorn --bind 0.0.0.0:$PORT app:app