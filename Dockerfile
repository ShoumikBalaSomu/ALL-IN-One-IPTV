# Stage 1: Build the Ktor Proxy Engine (Java/Kotlin)
FROM gradle:8.5-jdk17-alpine AS builder
WORKDIR /app
COPY proxy_app/ ./
# Run the Gradle build (shadowJar assuming it's configured in Ktor)
# RUN ./gradlew buildFatJar --no-daemon

# Stage 2: Final Multi-Arch Alpine Image
FROM alpine:latest

# Install dependencies for both the Aggregator (Python) and Proxy (Java)
RUN apk add --no-cache python3 py3-pip openjdk17-jre tzdata

WORKDIR /app

# Copy Python Backend (Phase 1)
COPY colab_encryptor.py .
COPY scraper.py .
COPY folder.py .
COPY checker.py .
COPY requirements.txt .

# Install Python requirements
RUN pip3 install --break-system-packages -r requirements.txt || pip3 install --break-system-packages aiohttp pycryptodome thefuzz

# Copy Java Proxy (Phase 3)
# COPY --from=builder /app/app/build/libs/*-all.jar /app/proxy.jar

# Expose Local Proxy Port
EXPOSE 8080

# Environment Variables
ENV ENV_PLAYLIST_KEY=""
ENV TZ="UTC"

# Run a start script that boots both the Proxy and Cron Aggregator
COPY start.sh .
RUN chmod +x start.sh

CMD ["./start.sh"]
