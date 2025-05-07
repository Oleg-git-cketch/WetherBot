import telebot
import requests
import json
import database as db
import buttons as bt
import os
from dotenv import load_dotenv

load_dotenv()  # Загружаем переменные из .env

TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(TOKEN)

API = 'ef0edd48014fd260a773940389f3aa9f'


@bot.message_handler(commands=['start'])
def start(message):

    user_id = message.from_user.id
    if db.check_user(user_id):
            bot.send_message(user_id, f'Привет, @{message.from_user.username}!\nНапишите название города:',
                         reply_markup=telebot.types.ReplyKeyboardRemove())
            bot.register_next_step_handler(message, get_weather)
    else:
        bot.send_message(user_id, 'Привет, давай начнем регистрацию! Введите имя:')
        bot.register_next_step_handler(message, get_name)

def get_name(message):
    user_id = message.from_user.id
    user_name = message.text
    bot.send_message(user_id, 'Отлично! Теперь отправьте свой номер через кнопку!',
                     reply_markup=bt.number_button())
    bot.register_next_step_handler(message, get_number, user_name)

def get_number(message, user_name):
    user_id = message.from_user.id
    if message.contact:
        user_number = message.contact.phone_number
        db.register(user_id, user_name, user_number)
        bot.send_message(user_id, '✅ Вы успешно зарегистрированы!✅\nПерезапустите бота - /start')
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(user_id, '❌ Ошибка! Отправьте свой номер через кнопку! ❌')
        bot.register_next_step_handler(user_id, get_name)

# def handle_location(message):
#     user_id = message.from_user.id
#     if message.location:
#         latitude = message.location.latitude
#         longitude = message.location.longitude
#         db.location(latitude, longitude)
#         bot.send_message(user_id, '✅ Вы успешно зарегистрированы!✅', reply_markup=telebot.types.ReplyKeyboardRemove())
#         bot.register_next_step_handler(message, start)




@bot.message_handler(content_types=['text'])
def get_weather(message):
    city = message.text.strip().lower()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
    if res.status_code == 200:
        data = json.loads(res.text)
        temp = data["main"]["temp"]
        if temp > 25.0:
            photo_path = 'hot.png'
            caption = f'Сейчас температура в городе "{city}" {temp}°C 🥵'
        elif temp < 5.0:
            photo_path = 'cold.png'
            caption = f'Сейчас температура в городе "{city}" {temp}°C 🥶'
        else:
            photo_path = 'cool.png'
            caption = f'Сейчас температура в городе "{city}" {temp}°C 🧣'

        with open(photo_path, 'rb') as photo:
            bot.send_photo(message.chat.id, photo, caption=caption)
    else:
        bot.send_message(message.chat.id, '❗ОШИБКА❗\nГород указан не верно!\nУкажите навание правильно!')


bot.polling()