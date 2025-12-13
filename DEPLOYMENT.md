# ShopKart Deployment Guide

## Quick Start - Go Live

### Option 1: Docker Deployment (Recommended)

1. **Build the Docker image:**
   ```bash
   docker build -t shopkart .
   ```

2. **Create `.env` file:**
   ```bash
   DJANGO_SECRET_KEY=your-secret-key-here
   DJANGO_DEBUG=False
   DJANGO_ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
   DB_ENGINE=django.db.backends.mysql
   DB_NAME=your_database
   DB_USER=your_user
   DB_PASSWORD=your_password
   DB_HOST=your_db_host
   DB_PORT=3306
   ```

3. **Run the container:**
   ```bash
   docker run -d -p 8000:8000 --env-file .env --name shopkart shopkart
   ```

4. **Access your site:**
   - Visit `http://your-server-ip:8000`

### Option 2: Traditional Server Deployment

#### Prerequisites
- Python 3.13+
- MySQL/MariaDB
- Nginx (recommended)

#### Steps

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment variables:**
   Create `.env` file with your production settings

3. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

4. **Create superuser:**
   ```bash
   python manage.py createsuperuser
   ```

5. **Populate products:**
   ```bash
   python manage.py populate_products
   ```

6. **Collect static files:**
   ```bash
   python manage.py collectstatic --noinput
   ```

7. **Start with Gunicorn:**
   ```bash
   gunicorn saros_project.wsgi --bind 0.0.0.0:8000 --workers 3
   ```

### Option 3: Platform Deployment

#### Heroku
```bash
heroku create your-app-name
heroku config:set DJANGO_SECRET_KEY=$(python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")
heroku config:set DJANGO_DEBUG=False
heroku config:set DJANGO_ALLOWED_HOSTS=your-app-name.herokuapp.com
heroku addons:create heroku-postgresql:hobby-dev
git push heroku main
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
heroku run python manage.py populate_products
```

#### Railway
1. Connect your GitHub repository
2. Set environment variables in Railway dashboard
3. Railway will auto-detect and deploy

#### Render
1. Create new Web Service
2. Connect your repository
3. Set build command: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
4. Set start command: `gunicorn saros_project.wsgi`
5. Add environment variables
6. Deploy!

## Environment Variables Required

| Variable | Description | Example |
|----------|-------------|---------|
| `DJANGO_SECRET_KEY` | Django secret key | Generate with Django |
| `DJANGO_DEBUG` | Debug mode | `False` for production |
| `DJANGO_ALLOWED_HOSTS` | Allowed domains | `yourdomain.com,www.yourdomain.com` |
| `DB_ENGINE` | Database engine | `django.db.backends.mysql` |
| `DB_NAME` | Database name | `shopkart_db` |
| `DB_USER` | Database user | `shopkart_user` |
| `DB_PASSWORD` | Database password | `secure_password` |
| `DB_HOST` | Database host | `localhost` or IP |
| `DB_PORT` | Database port | `3306` |

## Post-Deployment Checklist

- [ ] Set `DEBUG=False` in production
- [ ] Configure `ALLOWED_HOSTS` with your domain
- [ ] Set strong `SECRET_KEY`
- [ ] Configure production database
- [ ] Set up SSL/HTTPS certificate
- [ ] Configure domain DNS
- [ ] Set up backup system
- [ ] Configure email settings (for order notifications)
- [ ] Test all functionality
- [ ] Set up monitoring/logging

## Troubleshooting

### Static files not loading
- Run `python manage.py collectstatic`
- Check `STATIC_ROOT` and `STATIC_URL` in settings
- Verify WhiteNoise middleware is enabled

### Database connection errors
- Check database credentials in `.env`
- Verify database server is running
- Check firewall rules

### 500 errors
- Check `DEBUG=True` temporarily to see error details
- Review server logs
- Verify all environment variables are set

## Support

For issues, check:
- Django logs: `logs/` directory
- Server logs: Check your hosting platform logs
- Database logs: Check MySQL/MariaDB logs


