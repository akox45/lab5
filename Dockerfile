# syntax=docker/dockerfile:1
FROM python:3.11-slim

# Install system dependencies including OpenCV requirements
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libx11-6 \
    ffmpeg \
    libsm6 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=photoalbum.settings \
    OPENCV_VIDEOIO_PRIORITY_MSMF=0

# Create and set working directory
WORKDIR /app

# Install Python dependencies
COPY photoalbum/requirements.txt ./requirements.txt
RUN pip install --upgrade pip \
    && pip install opencv-python-headless \
    && pip install -r requirements.txt

# Copy application code
COPY photoalbum /app

# Create non-root user
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Collect static files
RUN python manage.py collectstatic --noinput

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8080/ || exit 1

# Start the application
CMD python manage.py migrate && \
    gunicorn photoalbum.wsgi:application --bind 0.0.0.0:8080 --workers 2 --threads 2 