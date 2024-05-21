from telebot import TeleBot

from database import DataBase
from telebot import apihelper

ip = '37.19.220.129'
port = '8443'

apihelper.proxy = {
  'https': 'socks5h://{}:{}'.format(ip, port)
}

token = DataBase.get_bot()[0]
bot = TeleBot('6570305935:AAGj3frXebsYNLFJelThSuBRDukcRWHz-Ig')
# print(bot.get_me())
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, text='Choose Option')

bot.infinity_polling(timeout=123, skip_pending=True)

# import requests
# import logging
# logging.basicConfig(level=logging.DEBUG)
# r = requests.get('https://api.telegram.org/bot6570305935:AAGj3frXebsYNLFJelThSuBRDukcRWHz-Ig/sendMessage?chat_id=-4033243626&text=%D0%92%D1%81%D0%B5%D0%BC%20%D0%BF%D1%80%D0%B8%D0%B2%D0%B5%D1%82!%20%D0%9F%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%BA%D0%B0%20%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D1%8B%20%D0%B1%D0%BE%D1%82%D0%B0')
# print(r)


