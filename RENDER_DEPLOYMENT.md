# Render Deployment Guide - Troubleshooting

## If you get "pip install" errors during build:

### Option 1: Use Python 3.12 (Recommended)
Render should automatically use `runtime.txt`. The file is set to Python 3.12.7 for better compatibility.

### Option 2: Update Build Command
In Render dashboard, change Build Command to:
```bash
pip install --upgrade pip setuptools wheel && pip install -r requirements.txt && python manage.py collectstatic --noinput
```

### Option 3: Use Alternative Requirements
If specific versions fail, temporarily use `requirements-alt.txt`:
1. Rename `requirements-alt.txt` to `requirements.txt`
2. Commit and push
3. Deploy again

### Option 4: Install packages one by one
If all else fails, use this Build Command:
```bash
pip install --upgrade pip setuptools wheel && \
pip install Django==5.2.8 && \
pip install Pillow && \
pip install requests && \
pip install psycopg2-binary && \
pip install gunicorn && \
pip install whitenoise && \
python manage.py collectstatic --noinput
```

## Render Configuration

### Build Command:
```bash
pip install -r requirements.txt && python manage.py collectstatic --noinput
```

### Start Command:
```bash
gunicorn saros_project.wsgi --bind 0.0.0.0:$PORT --workers 3 --timeout 120
```

### Environment Variables:
- `DJANGO_SECRET_KEY` - Your secret key
- `DJANGO_DEBUG=False`
- `DJANGO_ALLOWED_HOSTS=your-app-name.onrender.com`
- `DB_ENGINE=django.db.backends.postgresql`
- `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT` - From your Render PostgreSQL database

## Note about Docker
Render typically uses native builds, not Docker. If you're using Docker, make sure:
1. Docker is enabled in your Render service settings
2. The Dockerfile is correct (we've updated it to Python 3.12)
3. All dependencies are properly specified





































