# Use slim Python base image
FROM python:3.11-slim

# Environment variables to avoid pyc and enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install build tools if needed (for pip packages with C extensions)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies first (cached if unchanged)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code into container
COPY src/ ./src
COPY .env .
COPY README.md .

# ⚠️ Don’t bake secrets into the image!
# Instead, mount oauth_credentials.json + oauth_token.json at runtime

# Set default command
CMD ["python", "-m", "src.main"]
