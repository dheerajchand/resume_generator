FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Collect static files
RUN SECRET_KEY=build-only DEBUG=False python manage.py collectstatic --no-input 2>/dev/null || true

EXPOSE ${PORT:-8000}

CMD gunicorn resume_generator_django.wsgi --bind 0.0.0.0:${PORT:-8000} --workers 2 --threads 2 --log-file -
