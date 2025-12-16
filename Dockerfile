# 1. Base Image - Use a stable, slim version for smaller size
FROM python:3.12-slim

# 2. Set Environment Variables for Python optimization
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Set Working Directory
WORKDIR /app

# 4. Install System Dependencies required for psycopg2 compilation and running
# postgresql-client is included for debugging/migrations, which is good.
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    libpq-dev \
    python3-dev \
    # Clean up apt caches to keep the image size small
    && rm -rf /var/lib/apt/lists/*

# 5. Install Python Dependencies
# Copy requirements.txt first to leverage Docker's build cache
COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# 6. Copy Application Code
# Copy everything else now
COPY . .

# 7. Collect Static Files (Assuming a Django App)
# Note: Using '|| true' is a good defensive step for collectstatic in a Dockerfile.
RUN python manage.py collectstatic --noinput || true

# 8. Expose Port
EXPOSE 8000

# 9. Define the Startup Command (using gunicorn)
CMD ["gunicorn", "saros_project.wsgi", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "120"]