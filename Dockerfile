# Use Python 3.12 slim image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

ENV TRANSFORMERS_CACHE=/tmp/.cache
RUN mkdir -p /tmp/.cache && chmod -R 777 /tmp/.cache

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Expose port 7860 for Hugging Face Spaces
EXPOSE 7860

# Command to run your FastAPI app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]
