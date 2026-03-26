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

# Set default port (Render will override this with its own $PORT)
ENV PORT 10000
EXPOSE $PORT

# Start command (using shell form to allow environment variable expansion)
CMD gunicorn --bind 0.0.0.0:$PORT app:app
