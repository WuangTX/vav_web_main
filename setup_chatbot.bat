@echo off
echo ================================
echo VAV Furniture Chatbot Setup
echo ================================
echo.

echo Installing Python dependencies...
pip install cohere==5.5.8
pip install channels==4.0.0  
pip install channels-redis==4.2.0
pip install redis==5.0.1

echo.
echo Creating chatbot migrations...
python manage.py makemigrations chatbot

echo.
echo Running database migrations...
python manage.py migrate

echo.
echo ================================
echo Setup completed successfully!
echo ================================
echo.
echo You can now:
echo 1. Start the server: python manage.py runserver
echo 2. Visit /chatbot/ for full chatbot page
echo 3. Chatbot widget is available on all pages
echo.
echo For more information, see CHATBOT_GUIDE.md
echo.
pause
