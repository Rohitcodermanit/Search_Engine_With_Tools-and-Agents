FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy requirements first and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Streamlit config (prevents usage prompts)
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Expose the port for Hugging Face
EXPOSE 7860

# Healthcheck for Streamlit
HEALTHCHECK CMD curl --fail http://localhost:7860/_stcore/health || exit 1

# Run app.py by default
CMD ["streamlit", "run", "src/app.py", "--server.port=7860", "--server.address=0.0.0.0"]
