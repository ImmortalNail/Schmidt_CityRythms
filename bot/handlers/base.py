from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, ConversationHandler
from bot.utils.constants import MESSAGES, AGE_VERIFICATION, NAME

def start(update: Update, context: CallbackContext) -> int:
    keyboard = [
        [InlineKeyboardButton("Да", callback_data='age_yes'),
         InlineKeyboardButton("Нет", callback_data='age_no')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    update.message.reply_text(
        MESSAGES['age_verification'],
        reply_markup=reply_markup
    )
    
    return AGE_VERIFICATION

def age_verification(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    
    if query.data == 'age_no':
        query.edit_message_text(text=MESSAGES['age_rejected'])
        return ConversationHandler.END
    else:
        query.edit_message_text(text=MESSAGES['ask_name'])
        return NAME

def get_name(update: Update, context: CallbackContext) -> int:
    context.user_data['name'] = update.message.text
    update.message.reply_text(MESSAGES['greeting'].format(name=context.user_data['name']))
    update.message.reply_text(MESSAGES['ask_age'])
    return AGE