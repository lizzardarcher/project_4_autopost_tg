import traceback
from datetime import datetime, timedelta, time
from time import sleep
import sys
from telebot import TeleBot

from database import DataBase

from utils import djangoORM
from apps.home.models import MessageToSend, Bot, UserToMail

WEEKDAYS = {
    'mon': 0,
    'tue': 1,
    'wed': 2,
    'thu': 3,
    'fri': 4,
    'sat': 5,
    'sun': 6,
}

def post():
    bots = Bot.objects.all()
    message = MessageToSend.objects.get(id=1)
    users = UserToMail.objects.all()

    weekday = datetime.now().weekday()
    current_time = datetime.now().strftime('%H:%M')

    for bot in bots:
        bot = TeleBot(bot.token)
        if weekday == WEEKDAYS[message.day_to_send_1_first] or weekday == WEEKDAYS[message.day_to_send_1_second]:
            if current_time == message.time_to_send_1.strftime('%H:%M'):
                for user in users:
                    try:
                        bot.send_message(chat_id=user.id, text=message.message_1)
                    except:
                        print(traceback.format_exc())
                sleep(60/len(bots) - 1)

        if weekday == WEEKDAYS[message.day_to_send_2_first] or weekday == WEEKDAYS[message.day_to_send_2_second]:
            if current_time == message.time_to_send_2.strftime('%H:%M'):
                for user in users:
                    try:
                        bot.send_message(chat_id=user.id, text=message.message_2)
                    except:
                        print(traceback.format_exc())
                sleep(60/len(bots) - 1)

while True:
    try:
        post()
        sleep(1)
        sys.exit()
    except KeyboardInterrupt:
        print('Post Exit')
        print(KeyboardInterrupt)
