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
            "image_url": "https://www.ferrari.com/images/auto/FS_F8_Tributo_Motore_V8.jpg"
        },
        {
            "name": "Porsche 911 GT3",
            "description": "Легендарный спортивный автомобиль с высокими динамическими характеристиками.",
            "image_url": "https://files.porsche.com/filestore/image/multimedia/none/992-gt3-modelimage-sideshot/thumbwhite/189bf86d-e3ab-11eb-80cd-005056bbdc38;sP;twebp/porsche-thumbwhite.webp"
        },
        {
            "name": "Lamborghini Aventador",
            "description": "Итальянский суперкар с двигателем V12 и уникальным дизайном.",
            "image_url": "https://www.lamborghini.com/sites/it-en/files/DAM/lamborghini/model/aventador/aventador-s/2021/06_24/gallery/aventador-s-gallery-01.jpg"
        },
    ],
    "Классические": [
        {
            "name": "Ford Mustang 1965",
            "description": "Икона американского автомобилестроения середины 60-х годов.",
            "image_url": "https://upload.wikimedia.org/wikipedia/commons/6/6d/1965_Ford_Mustang_coupe_%28cropped%29.jpg"
        },
        {
            "name": "Chevrolet Camaro 1969",
            "description": "Классический маслкар с мощным двигателем и узнаваемым дизайном.",
            "image_url": "https://cdn.dealeraccelerate.com/vanguard/1/18317/107841/1920x1440/1969-chevrolet-camaro-ss.jpg"
        },
        {
            "name": "Volkswagen Beetle",
            "description": "Легендарный народный автомобиль, произведённый в Германии.",
            "image_url": "https://upload.wikimedia.org/wikipedia/commons/3/31/VW_Beetle-IMG_0508.jpg"
        },
    ],
    "Внедорожники": [
        {
            "name": "Land Rover Defender",
            "description": "Легендарный британский внедорожник с превосходными внедорожными качествами.",
            "image_url": "https://www.landrover.ru/Images/DEF_90_20MY_EXT_LOC01_JLR_CGI_09_RH_DynamicAngle_LR_RUP_3840x2160-v1_tcm296-694296.jpg"
        },
        {
            "name": "Jeep Wrangler",
            "description": "Американский внедорожник с богатой историей и отличной проходимостью.",
            "image_url": "https://www.jeep.com/content/dam/fca-brands/na/jeep/en_us/2021/wrangler/vlp/gallery/exterior/wrangler-vlp-gallery-exterior-1.jpg"
        },
        {
            "name": "Toyota Land Cruiser",
            "description": "Надёжный и прочный японский внедорожник, популярный по всему миру.",
            "image_url": "https://www.toyota.com/imgix/responsive/images/mlp/colorizer/2021/landcruiser/1G3/1.png"
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
