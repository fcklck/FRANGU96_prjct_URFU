#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Этот бот предоставляет информацию о случайных автомобилях на основе выбранной пользователем категории.
"""

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
from dotenv import load_dotenv  # Для загрузки переменных окружения

# Настройка логирования
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Определение состояний для ConversationHandler
CHOOSING = range(1)

# Клавиатура с категориями автомобилей
reply_keyboard = [
    ["Спортивные", "Классические"],
    ["Внедорожники", "Случайный"],
    ["Стоп"],
]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

# Словарь с данными об автомобилях
cars = {
    "Спортивные": [
        {
            "name": "Ferrari F8 Tributo",
            "description": "Итальянский суперкар с двигателем V8 и мощностью 720 л.с.",
            "image_url": "https://example.com/ferrari_f8.jpg"
        },
        {
            "name": "Porsche 911 GT3",
            "description": "Легендарный спортивный автомобиль с высокими динамическими характеристиками.",
            "image_url": "https://example.com/porsche_911.jpg"
        },
        # Добавьте больше автомобилей по желанию
    ],
    "Классические": [
        {
            "name": "Ford Mustang 1965",
            "description": "Икона американского автомобилестроения середины 60-х годов.",
            "image_url": "https://example.com/ford_mustang.jpg"
        },
        {
            "name": "Chevrolet Camaro 1969",
            "description": "Классический маслкар с мощным двигателем и узнаваемым дизайном.",
            "image_url": "https://example.com/chevrolet_camaro.jpg"
        },
        # Добавьте больше автомобилей по желанию
    ],
    "Внедорожники": [
        {
            "name": "Land Rover Defender",
            "description": "Легендарный британский внедорожник с превосходными внедорожными качествами.",
            "image_url": "https://example.com/land_rover_defender.jpg"
        },
        {
            "name": "Jeep Wrangler",
            "description": "Американский внедорожник с богатой историей и отличной проходимостью.",
            "image_url": "https://example.com/jeep_wrangler.jpg"
        },
        # Добавьте больше автомобилей по желанию
    ],
    "Случайный": [
        # Объединяем все категории для случайного выбора
    ]
}

# Объединяем все автомобили в категорию "Случайный"
cars["Случайный"] = sum(cars.values(), [])

def get_random_car(category: str) -> dict:
    """Получить информацию о случайном автомобиле из заданной категории."""
    logger.info(f"Запрос автомобиля для категории: {category}")

    if category in cars:
        car = random.choice(cars[category])
        logger.info(f"Выбран автомобиль: {car['name']}")
        return car
    else:
        logger.error(f"Неизвестная категория: {category}")
        return None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Начало разговора с пользователем."""
    user = update.message.from_user
    logger.info(f"Пользователь {user.full_name} начал разговор.")

    await update.message.reply_text(
        "Привет! Я бот, который расскажет вам об интересных автомобилях. Выберите категорию:",
        reply_markup=markup
    )

    return CHOOSING

async def regular_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработка выбора категории и отправка информации об автомобиле."""
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
    """Завершение разговора."""
    await update.message.reply_text("Спасибо за использование бота! До свидания!")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработка команды отмены."""
    await update.message.reply_text("Вы отменили разговор. До свидания!")
    return ConversationHandler.END

def main() -> None:
    """Запуск бота."""
    # Загрузка токена из файла .env
    load_dotenv()
    TOKEN = os.getenv("BOT_TOKEN")
    if not TOKEN:
        logger.error("Токен бота не найден. Пожалуйста, установите переменную окружения BOT_TOKEN.")
        return

    application = Application.builder().token(TOKEN).build()

    # Определение обработчиков
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CHOOSING: [MessageHandler(filters.TEXT & ~filters.COMMAND, regular_choice)],
        },
        fallbacks=[CommandHandler("done", done), CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()
