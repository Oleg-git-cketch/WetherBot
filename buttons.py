from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def number_button():
 markup = ReplyKeyboardMarkup(resize_keyboard=True)
 but1= KeyboardButton(text="Отправить номер телефона 📞", request_contact=True)
 # but2 = KeyboardButton(text="Отправить локацию ♦️", request_location=True)
 markup.add(but1)
 return markup

def menu_buttons():
 kb = ReplyKeyboardMarkup(resize_keyboard=True)
 but1 = KeyboardButton('Узнать погоду☀️')
 but2 = KeyboardButton('Авто рассылка погоды')
 but3 = KeyboardButton('Настройки (coming soon)')
 kb.add(but1, but3)
 kb.row(but2)
 return kb