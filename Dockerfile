# TechScale: Multi-stage Docker build

# Stage 1: Builder
FROM python:3.11-slim AS builder

WORKDIR /build

COPY requirements.txt .

RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# Stage 2: Runtime
FROM python:3.11-slim

WORKDIR /app

# Copy only installed dependencies
COPY --from=builder /install /usr/local

# Copy application source
COPY app/ .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]