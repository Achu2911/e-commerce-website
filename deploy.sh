#!/bin/bash
# Deployment script for ShopKart

echo "🚀 Starting ShopKart deployment..."

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found!"
    echo "Please copy .env.example to .env and configure it."
    exit 1
fi

# Load environment variables
export $(cat .env | grep -v '^#' | xargs)

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Run migrations
echo "🗄️ Running database migrations..."
python manage.py migrate

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Create superuser if needed
echo "👤 Checking for superuser..."
python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(is_superuser=True).exists():
    print("⚠️  No superuser found. Please run: python manage.py createsuperuser")
else:
    print("✅ Superuser exists")
EOF

# Populate products if database is empty
echo "🛍️ Checking products..."
python manage.py shell << EOF
from shop.models import Product
if Product.objects.count() == 0:
    print("📦 Populating products...")
    import subprocess
    subprocess.call(['python', 'manage.py', 'populate_products'])
else:
    print("✅ Products exist")
EOF

echo "✅ Deployment preparation complete!"
echo ""
echo "To start the server:"
echo "  Development: python manage.py runserver"
echo "  Production:  gunicorn saros_project.wsgi --bind 0.0.0.0:8000"


