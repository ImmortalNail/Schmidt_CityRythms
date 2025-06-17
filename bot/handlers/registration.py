from telegram import Update
from telegram.ext import CallbackContext
from bot.utils.constants import AGE, MESSAGES
from bot.handlers.routes import show_routes

def get_age(update: Update, context: CallbackContext) -> int:
    try:
        age = int(update.message.text)
        if age < 18:
            update.message.reply_text(MESSAGES['age_rejected'])
            return ConversationHandler.END
        context.user_data['age'] = age
        return show_routes(update, context)
    except ValueError:
        update.message.reply_text(MESSAGES['invalid_age'])
        return AGE