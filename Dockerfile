FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY agency ./agency
COPY .env.example .env

# Create non-root user for security
RUN useradd -m appuser && chown -R appuser /app
USER appuser

# Entrypoint to run the Hunter
ENTRYPOINT ["python", "-m", "agency.hunter.main"]
CMD ["--keyword=logistics companies chile", "--limit=5", "--proof"]
