import os
import json
import random
from telegram import Update, InputMediaPhoto
from telegram.ext import Updater, CommandHandler, CallbackContext
import logging
import os

from dotenv import load_dotenv
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
with open('cars.json', 'r', encoding='utf-8') as f:
    cars_data = json.load(f)
    from telegram.ext import CommandHandler, MessageHandler, Filters

def start(update: Update, context: CallbackContext):
    update.message.reply_text('Привет! Отправь команду /car, чтобы получить интересный автомобиль.')

def send_random_car(update: Update, context: CallbackContext):
    car = random.choice(cars_data)
    message = f"*{car['name']}*\n{car['description']}"
    photo_url = car['image_url']
    update.message.reply_photo(photo=photo_url, caption=message, parse_mode='Markdown')

def unknown_command(update: Update, context: CallbackContext):
    update.message.reply_text('Извините, я не знаю такой команды. Используйте /car, чтобы получить интересный автомобиль.')
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('car', send_random_car))
    dp.add_handler(MessageHandler(Filters.command, unknown_command))

    updater.start_polling()
    updater.idle()


from telegram import Update, BotCommand
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    filters
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """start template"""
    pass

async def command1(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    pass

async def command2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    pass


# Функция для регистрации команд в BotFather
async def post_init(application: Application) -> None:
    bot_commands = [
        BotCommand("start", "Начало работы с ботом")
    ]
    await application.bot.set_my_commands(bot_commands)

def main() -> None:
    """"""   
    # создаем приложение 
    application = Application.builder().token(os.getenv("BOT_TOKEN")).post_init(post_init).build()

    # добавляем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("command1", command1))
    application.add_handler(CommandHandler("command2", command2))

    # можно добавить отдельные обработки чего угодно
    # сообщения, но не команды
    ## application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    # местоположения
    ## application.add_handler(MessageHandler(filters.LOCATION, location))
    # изображения
    ## application.add_handler(MessageHandler(filters.ATTACHMENT, attachment))
    # и тд

    # Запускаем до нажатия Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
