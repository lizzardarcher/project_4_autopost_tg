from utils import djangoORM
from apps.home.models import Post, Bot, Chat

import traceback
from time import sleep
from datetime import date, datetime, timedelta
import sys
import logging
from telebot import TeleBot

logging.basicConfig(filename='log.log', level=logging.WARNING)

# MEDIA_ROOT = 'static/media/'
MEDIA_ROOT = '/var/www/html/main/core/static/media/'

def post():
    bots = Bot.objects.all()
    for b in bots:
        bot = TeleBot(token=b.token)

        chats = Chat.objects.filter(bot=b) # Все чаты
        messages = Post.objects.filter(is_sent=False, is_for_sched=True, bot=b)
        for message in messages:
            text = message.text
            mediafile = message.media_file.name
            post_time_for_schedule = message.sched_datetime
            server_time = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M')
            try:
                if post_time_for_schedule.strftime('%Y-%m-%d %H:%M') == server_time:

                    for chat in chats:  # По всем чатам
                        chat_reference = chat.reference
                        try:
                            chat_num_id = chat.chat_id
                        except:
                            chat_num_id = chat_reference
                        try:
                            if 'jpg' in mediafile or 'jpeg' in mediafile:
                                bot.send_photo(chat_id=chat_num_id, photo=open(MEDIA_ROOT + mediafile, 'rb'),
                                               caption=text,
                                               parse_mode='HTML')
                            elif 'mp3' in mediafile:
                                bot.send_audio(chat_id=chat_num_id, audio=open(MEDIA_ROOT + mediafile, 'rb'),
                                               caption=text,
                                               parse_mode='HTML')
                            elif 'mp4' in mediafile or 'mpeg' in mediafile or 'avi' in mediafile or 'mkv' in mediafile:
                                bot.send_video(chat_id=chat_num_id, video=open(MEDIA_ROOT + mediafile, 'rb'),
                                               caption=text,
                                               parse_mode='HTML')
                            else:
                                bot.send_message(chat_id=chat_num_id, text=text, parse_mode='HTML')
                            chat.error = ''
                            chat.save()
                        except:
                            print(traceback.format_exc())
                            if '403' in traceback.format_exc():
                                chat.error = 'Ошибка 403 Бот не являестся администратором группы(канала)'
                                chat.save()
                    message.is_sent = True
                    message.save()
            except:
                print(traceback.format_exc())



if __name__ == '__main__':
    try:
        while True:
            post()
            sleep(5)
    except KeyboardInterrupt:
        print('Post Failed')
        print(KeyboardInterrupt)
