import os
from pytz import timezone

class Config:
    # Основные настройки
    TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    TIMEZONE = timezone('Europe/Moscow')
    
    # Google API
    GOOGLE_CREDS = 'credentials.json'
    SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')
    DRIVE_FOLDER_ID = os.getenv('DRIVE_FOLDER_ID')
    
    # Режим работы
    WEBHOOK_MODE = os.getenv('WEBHOOK_MODE', 'False').lower() == 'true'
    PORT = int(os.getenv('PORT', 5000))
    ADMIN_PORT = int(os.getenv('ADMIN_PORT', 5001))
    
    # Вебхук (если включен)
    WEBHOOK_URL = os.getenv('WEBHOOK_URL', 'https://your-render-app.onrender.com')
    
    # Настройки для Render
    HOST = '0.0.0.0'