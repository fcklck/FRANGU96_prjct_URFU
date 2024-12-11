#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
import random
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)
from dotenv import load_dotenv

# Настройка базового логирования для консоли
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Создание и настройка FileHandler
file_handler = logging.FileHandler('./data/bot.log')
file_handler.setLevel(logging.INFO)

# Создание форматтера и добавление его к FileHandler
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

# Добавление FileHandler к логгеру
logger.addHandler(file_handler)
CHOOSING = range(1)

reply_keyboard = [
    ["Спортивные", "Классические"],
    ["Внедорожники", "Случайный"],
    ["Стоп"],
]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

cars = {
    "Спортивные": [
        {
            "name": "Ferrari F8 Tributo",
            "description": "Итальянский суперкар с двигателем V8 и мощностью 720 л.с.",
            "image_url": "https://getmecar.ru/wp-content/uploads/2023/11/20-2-3.webp"
        },
        {
            "name": "Porsche 911 GT3",
            "description": "Легендарный спортивный автомобиль с высокими динамическими характеристиками.",
            "image_url": "https://avatars.mds.yandex.net/i?id=8e08adeb04b070a8440bcd27b482c159_l-4452791-images-thumbs&n=13"
        },
        {
            "name": "Lamborghini Aventador",
            "description": "Итальянский суперкар с двигателем V12 и уникальным дизайном.",
            "image_url": "https://autopeople.ru/news/wp-content/uploads/lamborghini-aventador-lp700-4-1781-1024x768.jpg"
        },
    ],
    "Классические": [
        {
            "name": "Ford Mustang 1965",
            "description": "Икона американского автомобилестроения середины 60-х годов.",
            "image_url": "https://a.d-cd.net/884b86s-960.jpg"
        },
        {
            "name": "Chevrolet Camaro 1969",
            "description": "Классический маслкар с мощным двигателем и узнаваемым дизайном.",
            "image_url": "https://w0.peakpx.com/wallpaper/1013/333/HD-wallpaper-1969-camaro-rs-ss-big-block-silver-classic-gm-bowtie-muscle.jpg"
        },
        {
            "name": "Volkswagen Beetle",
            "description": "Легендарный народный автомобиль, произведённый в Германии.",
            "image_url": "https://i.pinimg.com/originals/ef/b0/57/efb057b14c8186635a8d894d6a64e0a1.png"
        },
    ],
    "Внедорожники": [
        {
            "name": "Land Rover Defender",
            "description": "Легендарный британский внедорожник с превосходными внедорожными качествами.",
            "image_url": "https://avatars.dzeninfra.ru/get-zen_doc/1581919/pub_60f8e734ec3b0a41ed1b8f5d_60f8eea125ddc562e5fccd9a/scale_1200"
        },
        {
            "name": "Jeep Wrangler",
            "description": "Американский внедорожник с богатой историей и отличной проходимостью.",
            "image_url": "https://a.d-cd.net/YvQAAgDTG-A-1920.jpg"
        },
        {
            "name": "Toyota Land Cruiser",
            "description": "Надёжный и прочный японский внедорожник, популярный по всему миру.",
            "image_url": "https://avatars.mds.yandex.net/get-autoru-vos/2172109/3cde3307b0d0c0aae9edafce586393b9/1200x900"
        },
    ],
}

# Объединяем все автомобили для категории "Случайный"
cars["Случайный"] = sum(cars.values(), [])

def get_random_car(category: str) -> dict:
    logger.info(f"Запрос автомобиля для категории: {category}")
    if category in cars:
        car = random.choice(cars[category])
        logger.info(f"Выбран автомобиль: {car['name']}")
        return car
    else:
        logger.error(f"Неизвестная категория: {category}")
        return None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    logger.info(f"Пользователь {user.full_name} начал разговор.")
    await update.message.reply_text(
        "Привет! Я бот, который расскажет вам об интересных автомобилях. Выберите категорию:",
        reply_markup=markup
    )
    return CHOOSING

async def regular_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    category = update.message.text
    if category == "Стоп":
        await update.message.reply_text("Вы остановили бота. Чтобы начать снова, введите /start.")
        return ConversationHandler.END
    car = get_random_car(category)
    if car:
        message = f"*{car['name']}*\n{car['description']}"
        photo_url = car.get('image_url')
        if photo_url:
            await update.message.reply_photo(photo=photo_url, caption=message, parse_mode='Markdown')
        else:
            await update.message.reply_text(message, parse_mode='Markdown')
    else:
        await update.message.reply_text("Извините, не удалось найти автомобиль в этой категории.")
    return CHOOSING

async def done(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Спасибо за использование бота! До свидания!")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Вы отменили разговор. До свидания!")
    return ConversationHandler.END

def main() -> None:
    load_dotenv()
    TOKEN = os.getenv("BOT_TOKEN")
    if not TOKEN:
        logger.error("Токен бота не найден. Пожалуйста, установите переменную окружения BOT_TOKEN.")
        return
    application = Application.builder().token(TOKEN).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CHOOSING: [MessageHandler(filters.TEXT & ~filters.COMMAND, regular_choice)],
        },
        fallbacks=[CommandHandler("done", done), CommandHandler("cancel", cancel)],
    )
    application.add_handler(conv_handler)
    application.run_polling()

if __name__ == '__main__':
    main()
