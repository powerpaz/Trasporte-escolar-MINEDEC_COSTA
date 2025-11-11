# syntax=docker/dockerfile:1
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Install system deps (optional: add build-essential if needed for pandas)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates curl && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /app/

# Default port used by many PaaS (overridden by env PORT)
ENV PORT=8080
EXPOSE 8080

# Use gunicorn in production
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]