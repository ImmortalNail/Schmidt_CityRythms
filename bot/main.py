import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, ConversationHandler
from bot.handlers import (
    start, age_verification, get_name, get_age,
    show_routes, route_selected, confirm_participation, handle_photo
)
from bot.utils.constants import (
    AGE_VERIFICATION, NAME, AGE, ROUTE_SELECTION, PHOTO_UPLOAD
)
from config import Config
from admin_panel.app import app as admin_app
import threading
from flask import Flask
from telegram import Bot

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def run_bot():
    """Запуск Telegram бота"""
    updater = Updater(Config.TOKEN)
    dispatcher = updater.dispatcher

    # Обработчик диалога
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            AGE_VERIFICATION: [CallbackQueryHandler(age_verification)],
            NAME: [MessageHandler(Filters.text & ~Filters.command, get_name)],
            AGE: [MessageHandler(Filters.text & ~Filters.command, get_age)],
            ROUTE_SELECTION: [CallbackQueryHandler(route_selected)],
            PHOTO_UPLOAD: [
                MessageHandler(Filters.photo, handle_photo),
                CommandHandler('start', start)
            ],
        },
        fallbacks=[CommandHandler('start', start)],
    )

    dispatcher.add_handler(conv_handler)

    # Постоянное меню
    def setup_main_menu():
        from telegram import ReplyKeyboardMarkup
        menu_options = [
            ['📍 Информация о маршрутах'],
            ['📤 Загрузить фото паспорта участника'],
            ['ℹ Узнать больше']
        ]
        reply_markup = ReplyKeyboardMarkup(menu_options, resize_keyboard=True)

        def show_menu(update: Update, context: CallbackContext):
            update.message.reply_text(
                "Выберите опцию:",
                reply_markup=reply_markup
            )

        dispatcher.add_handler(MessageHandler(Filters.regex('^📍 Информация о маршрутах$'), show_routes))
        dispatcher.add_handler(MessageHandler(Filters.regex('^📤 Загрузить фото паспорта участника$'), 
                                lambda u,c: u.message.reply_text("Отправьте фото вашего паспорта с отметкой бара.")))
        dispatcher.add_handler(MessageHandler(Filters.regex('^ℹ Узнать больше$'), 
                                lambda u,c: u.message.reply_text("Подробнее: https://example.com")))

    setup_main_menu()

    # Режим работы (вебхук или поллинг)
    if Config.WEBHOOK_MODE:
        # Настройка вебхука
        updater.start_webhook(
            listen="0.0.0.0",
            port=Config.PORT,
            url_path=Config.TOKEN,
            webhook_url=f"{Config.WEBHOOK_URL}/{Config.TOKEN}"
        )
        logger.info("Бот запущен в режиме вебхука")
    else:
        # Обычный поллинг
        updater.start_polling()
        logger.info("Бот запущен в режиме поллинга")

    updater.idle()

def run_admin():
    """Запуск Flask админ-панели"""
    admin_app.run(host='0.0.0.0', port=Config.ADMIN_PORT, debug=False)

def main():
    # Запуск бота и админки в разных потоках
    bot_thread = threading.Thread(target=run_bot)
    admin_thread = threading.Thread(target=run_admin)

    bot_thread.start()
    admin_thread.start()

    bot_thread.join()
    admin_thread.join()

if __name__ == '__main__':
    main()