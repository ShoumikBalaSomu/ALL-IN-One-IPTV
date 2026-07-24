# Build stage
FROM python:3.11-slim AS builder

WORKDIR /app
COPY engine/requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Final stage
FROM python:3.11-slim

LABEL maintainer="ShoumikBalaSomu"
LABEL description="ALL-IN-ONE IPTV Engine (Year 3050 Spec)"

WORKDIR /app

# Copy dependencies
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Copy application code
COPY engine/ ./engine/
COPY input/ ./input/
COPY output/ ./output/

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python3 -c "import sys; sys.exit(0)"

CMD ["python3", "-m", "engine.src.main"]
