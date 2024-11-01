import traceback
from datetime import datetime, timedelta, time
from time import sleep
import sys
from telebot import TeleBot

from database import DataBase

text_1 = '''
Добрый вечер !!!
Надеемся что мы вместе продвигаемся к твоей цели.
🙌🙌🙌🙌🙌💪💪💪💪💪💪

Завтра утром ждём фото веса!👌
'''

text_2 = '''
Доброе утро!!!🙂😍😜
Сегодня контрольное взвешивание.

Пришлите в группу марафона фото  веса
'''

def post():
    bots = DataBase.get_bots()
    weekday = (datetime.now() + timedelta(days=0)).weekday()
    current_time = str(datetime.now().hour) + ':' + str(datetime.now().minute)
    for b in bots:
        bot = TeleBot(b[0])
        print(weekday, current_time)
        if weekday == 0 or weekday == 3:  # 0 & 3
            if current_time == '20:0':
                user_ids = DataBase.get_user_to_mail()
                for user_id in user_ids:
                    try:
                        bot.send_message(chat_id=user_id[0], text=text_1)
                    except:
                        print(traceback.format_exc())
                sleep(60/len(bots))
        elif weekday == 1 or weekday == 4:  # 1 & 4
            if current_time == '7:0':
                user_ids = DataBase.get_user_to_mail()
                for user_id in user_ids:
                    try:
                        bot.send_message(chat_id=user_id[0], text=text_2)
                    except:
                        print(traceback.format_exc())
                sleep(60/len(bots))

while True:
    try:
        post()
        sleep(1)
        sys.exit()
    except KeyboardInterrupt:
        ...
        # print(traceback.format_exc())
# for i in range(15):
#     post()
#     sleep(1)