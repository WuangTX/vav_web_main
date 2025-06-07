@echo off
echo ===================================
echo VAV Furniture - Django Server Setup
echo ===================================

echo.
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Initializing PostgreSQL database...
echo Make sure PostgreSQL is running and a database named 'vav_furniture' exists.
echo If not, please run these commands in PostgreSQL:
echo     CREATE DATABASE vav_furniture;
echo     ALTER USER postgres WITH PASSWORD 'postgres';

echo.
echo Making migrations for the main app...
python manage.py makemigrations main

echo.
echo Applying migrations...
python manage.py migrate

echo.
echo Loading sample data...
python manage.py loaddata sample_data

echo.
echo Setting up admin user (if needed)...
python -c "from django.contrib.auth.models import User; User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'adminpassword')"
echo Admin credentials:
echo   Username: admin
echo   Password: adminpassword
echo.

echo Starting the development server...
python manage.py runserver

echo.
echo Access the website at http://127.0.0.1:8000/
echo Access the admin panel at http://127.0.0.1:8000/admin/
echo Access the custom dashboard at http://127.0.0.1:8000/dashboard/
