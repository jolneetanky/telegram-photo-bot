# Use slim Python image
FROM python:3.11-slim

# Prevents Python from writing .pyc files and forces unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set working directory inside container
WORKDIR /app

# Install system dependencies if needed (build tools, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency list first for caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Run the app
CMD ["python", "src/main.py"]
