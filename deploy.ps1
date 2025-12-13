# PowerShell deployment script for ShopKart (Windows)

Write-Host "🚀 Starting ShopKart deployment..." -ForegroundColor Green

# Check if .env exists
if (-not (Test-Path .env)) {
    Write-Host "❌ Error: .env file not found!" -ForegroundColor Red
    Write-Host "Please create .env file with your configuration." -ForegroundColor Yellow
    exit 1
}

# Install dependencies
Write-Host "📦 Installing dependencies..." -ForegroundColor Cyan
pip install -r requirements.txt

# Run migrations
Write-Host "🗄️ Running database migrations..." -ForegroundColor Cyan
python manage.py migrate

# Collect static files
Write-Host "📁 Collecting static files..." -ForegroundColor Cyan
python manage.py collectstatic --noinput

Write-Host "✅ Deployment preparation complete!" -ForegroundColor Green
Write-Host ""
Write-Host "To start the server:" -ForegroundColor Yellow
Write-Host "  Development: python manage.py runserver" -ForegroundColor White
Write-Host "  Production:  gunicorn saros_project.wsgi --bind 0.0.0.0:8000" -ForegroundColor White


