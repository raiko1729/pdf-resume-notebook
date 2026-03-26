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

# Create directories for uploads and outputs
RUN mkdir -p uploads outputs

# Expose port
EXPOSE 10000

# Start command (using gunicorn)
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "app:app"]
