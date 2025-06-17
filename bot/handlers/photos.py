from telegram import Update
from telegram.ext import CallbackContext
from bot.utils.constants import PHOTO_UPLOAD, MESSAGES
from bot.services.gsheets import GoogleSheetsService
from bot.services.gdrive import GoogleDriveService
import logging

def handle_photo(update: Update, context: CallbackContext) -> int:
    photo_file = update.message.photo[-1].get_file()
    
    try:
        # Save to Google Drive
        gdrive = GoogleDriveService()
        file_url = gdrive.upload_photo(
            photo_file=photo_file,
            user_id=update.effective_user.id
        )
        
        # Update Google Sheets
        gsheets = GoogleSheetsService()
        gsheets.update_photo_count(update.effective_user.id)
        
        update.message.reply_text(MESSAGES['photo_received'])
    except Exception as e:
        logging.error(f"Photo upload error: {e}")
        update.message.reply_text("Ошибка при обработке фото. Попробуйте позже.")
    
    return PHOTO_UPLOAD