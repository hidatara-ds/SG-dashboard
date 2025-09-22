FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# System deps
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps first for caching
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy source
COPY flask_api ./flask_api
COPY gunicorn_config.py ./gunicorn_config.py

# Expose default port (Railway sets PORT env at runtime)
EXPOSE 5000

# Default envs
ENV FLASK_ENV=production \
    NODE_ENV=production \
    PORT=5000

# Run with gunicorn
CMD ["gunicorn", "-c", "gunicorn_config.py", "flask_api.wsgi:app"]


