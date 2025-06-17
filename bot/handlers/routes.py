from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from bot.utils.constants import ROUTE_SELECTION, PHOTO_UPLOAD, MESSAGES, ROUTES
from bot.services.gsheets import GoogleSheetsService

def show_routes(update: Update, context: CallbackContext) -> int:
    keyboard = [
        [InlineKeyboardButton(route['name'], callback_data=f'route_{route_id}')
        for route_id, route in ROUTES.items()
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    update.message.reply_text(MESSAGES['tour_description'])
    update.message.reply_text(
        MESSAGES['route_selection'],
        reply_markup=reply_markup
    )
    
    return ROUTE_SELECTION

def route_selected(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    
    route_key = query.data.split('_')[1]
    route = ROUTES[route_key]
    context.user_data['route'] = route_key
    
    # Send route info
    query.edit_message_text(text=f"Вы выбрали: {route['name']}")
    context.bot.send_message(
        chat_id=query.message.chat_id,
        text=f"{route['description']}\n\nБары на маршруте:\n{', '.join(route['bars'])}"
    )
    
    # Send participation buttons
    keyboard = [
        [InlineKeyboardButton("Выбрать другой маршрут", callback_data='change_route'),
         InlineKeyboardButton("Класс, я участвую", callback_data='confirm_participation')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    context.bot.send_message(
        chat_id=query.message.chat_id,
        text="Что вы хотите сделать дальше?",
        reply_markup=reply_markup
    )
    
    return ROUTE_SELECTION

def confirm_participation(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    
    if query.data == 'change_route':
        return show_routes(update, context)
    
    # Save participant data
    gsheets = GoogleSheetsService()
    user_data = context.user_data
    gsheets.add_participant(
        user_id=update.effective_user.id,
        name=user_data.get('name', ''),
        age=user_data.get('age', ''),
        route=user_data.get('route', '')
    )
    
    query.edit_message_text(text=MESSAGES['participation_instructions'])
    return PHOTO_UPLOAD