import traceback
import subprocess
from time import sleep
from datetime import date, datetime, timedelta
import sys

from telebot import TeleBot

from database import DataBase

# MEDIA_ROOT = 'static/media/'
# MEDIA_ROOT = '/var/www/html/main/core/static/media/'



token = DataBase.get_bot()[0]

bot = TeleBot(token)

bot.send_message(chat_id=-1001809639655, text='11221')