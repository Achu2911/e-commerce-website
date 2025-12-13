# ShopKart - E-Commerce Website

A modern, responsive e-commerce website built with Django for hair care products.

## Features

- 🛍️ Product catalog with categories
- 🛒 Shopping cart functionality
- 💳 Checkout system
- 📦 Order management
- 👤 User authentication
- 📱 Responsive design (Desktop & Mobile)
- 🎨 Modern UI with Bootstrap 5

## Tech Stack

- **Backend:** Django 5.2.8
- **Database:** MySQL (configurable)
- **Frontend:** Bootstrap 5, Custom CSS/JS
- **Server:** Gunicorn
- **Static Files:** WhiteNoise

## Installation

### Local Development

1. Clone the repository
```bash
git clone <your-repo-url>
cd shopkart
```

2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Configure environment variables
```bash
cp .env.example .env
# Edit .env with your settings
```

5. Run migrations
```bash
python manage.py migrate
```

6. Create superuser
```bash
python manage.py createsuperuser
```

7. Populate products (optional)
```bash
python manage.py populate_products
```

8. Run development server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/`

## Deployment

### Using Docker

1. Build the image
```bash
docker build -t shopkart .
```

2. Run the container
```bash
docker run -d -p 8000:8000 --env-file .env shopkart
```

### Using Gunicorn

1. Collect static files
```bash
python manage.py collectstatic
```

2. Run with Gunicorn
```bash
gunicorn saros_project.wsgi --bind 0.0.0.0:8000
```

### Platform-Specific Deployment

#### Heroku
```bash
heroku create your-app-name
heroku config:set DJANGO_SECRET_KEY=your-secret-key
heroku config:set DJANGO_DEBUG=False
heroku config:set DJANGO_ALLOWED_HOSTS=your-app-name.herokuapp.com
git push heroku main
```

#### Railway/Render
- Set environment variables in platform dashboard
- Connect your repository
- Deploy automatically

## Environment Variables

See `.env.example` for required environment variables:

- `DJANGO_SECRET_KEY` - Django secret key
- `DJANGO_DEBUG` - Debug mode (False for production)
- `DJANGO_ALLOWED_HOSTS` - Comma-separated list of allowed hosts
- `DB_*` - Database configuration

## Project Structure

```
shopkart/
├── shop/              # Main application
│   ├── models.py      # Database models
│   ├── views.py       # View functions
│   ├── templates/     # HTML templates
│   └── management/    # Management commands
├── saros_project/     # Project settings
├── static/            # Static files (CSS, JS)
├── media/             # User uploaded files
└── requirements.txt   # Python dependencies
```

## License

MIT License


