# Base Python image
FROM python:3.12.0-slim

# Set working directory
WORKDIR /app

# Copy requirements if available
COPY requirements.txt /app/requirements.txt

# Install system dependencies (if needed for NLP/search engines)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
# Install Python dependencies
COPY src/ ./src/
RUN pip install -r requirements.txt

# Copy all project files
COPY . /app

# Expose default port for Hugging Face Spaces
EXPOSE 8051

HEALTHCHECK CMD curl --fail http://localhost:8051/_stcore/health

ENTRYPOINT [ "streamlit", "run", "src/main.py", "--server.port=8051", "--server.address=0.0.0.0" ]
