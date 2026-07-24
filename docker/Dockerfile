# Stage 1: Build
FROM python:3.12-slim AS builder

WORKDIR /app
COPY requirements.txt .

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Production
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/home/appuser/.local/bin:${PATH}"

RUN groupadd -r appuser && useradd -r -g appuser -d /home/appuser -s /sbin/nologin -c "App User" appuser \
    && mkdir -p /home/appuser/.local /app/output \
    && chown -R appuser:appuser /home/appuser /app

WORKDIR /app

COPY --from=builder /root/.local /home/appuser/.local
COPY . .

RUN chown -R appuser:appuser /app

USER appuser

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/health')" || exit 1

CMD ["python", "-m", "engine.src.main"]
