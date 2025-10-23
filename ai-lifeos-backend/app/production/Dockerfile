# app/production/Dockerfile

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Prevents Python from writing pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1
# Prevents Python from buffering stdout/stderr
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY ../../requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend source code
COPY ../.. .

# Expose port
EXPOSE 8000

# Run the app
CMD ["bash", "app/production/start.sh"]
