# import os
# import django
# os.environ['DJANGO_SETTINGS_MODULE'] = 'core.settings'
# os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
# django.setup()

import traceback
import subprocess
from time import sleep
from datetime import date, datetime, timedelta
import sys
import logging
from telebot import TeleBot

from database import DataBase

logging.basicConfig(filename='log.log', level=logging.WARNING)

# MEDIA_ROOT = 'static/media/'
MEDIA_ROOT = '/var/www/html/main/core/static/media/'


def post():
    # print('started')
    bots = DataBase.get_bots()
    for b in bots:
        token = b[0]
        bot = TeleBot(token=token)
        # post_bot = DataBase.get_bot()
        start_date_bot = b[1]  # дата старта бота
        is_start_date_bot = b[1] == str(date.today())  # совпадает ли дата старта с сегодняшней
        is_bot_active = b[2]  # активен ли бот
        post_bot_day = b[3]  # день постинга у бота
        bot_id = b[4]
        # Если бот активен и дата старта совпадает с сегодняшней
        if is_start_date_bot and is_bot_active:

            chats = DataBase.get_chats_for_post_by_bot(bot_id)  # Все чаты

            # Посты. Неотправленные и у которых день постинга совпадает с днём у бота
            messages = DataBase.get_posts_by_bot_id((False, post_bot_day, bot_id))

            # Опрос. Неотправленные и у которых день постинга совпадает с днём у бота
            polls = DataBase.get_polls_by_bot_id((False, post_bot_day, bot_id))

            m_id = []
            poll_id = []
            for chat in chats:  # По всем чатам
                chat_reference = chat[0]
                chat_day = chat[1]
                # print(chat)
                try:
                    chat_num_id = chat[2]
                except:
                    chat_num_id = chat_reference

                # if chat_day <= post_bot_day:
                for message in messages:  # По всем одобренным сообщениям
                    message_day = message[0]
                    text = message[1]
                    mediafile = message[2]
                    post_time = message[3]
                    message_id = message[-1]
                    post_time_init = datetime.strptime(post_time, '%H:%M:%S').strftime('%H:%M')
                    server_time = datetime.strftime(datetime.now(), '%H:%M')
                    server_time_plus = datetime.strftime(datetime.now() + timedelta(minutes=3), '%H:%M')
                    # if datetime.strptime(post_time, '%H:%M:%S').strftime('%H:%M') == datetime.now().strftime('%H:%M') and message_day == post_bot_day:
                    # print(post_time_init, datetime.now().strftime('%H:%M'), server_time_plus)
                    if post_time_init >= datetime.now().strftime(
                            '%H:%M') and post_time_init < server_time_plus and message_day == post_bot_day:
                        try:
                            print('Posting accepted', message_id)
                            if 'jpg' in mediafile or 'jpeg' in mediafile:
                                bot.send_photo(chat_id=chat_num_id, photo=open(MEDIA_ROOT + mediafile, 'rb'),
                                               caption=text,
                                               parse_mode='HTML')
                                # print('Photo sent')
                            elif 'mp3' in mediafile:
                                bot.send_audio(chat_id=chat_num_id, audio=open(MEDIA_ROOT + mediafile, 'rb'),
                                               caption=text,
                                               parse_mode='HTML')
                                # print('audio sent')
                            elif 'mp4' in mediafile or 'mpeg' in mediafile or 'avi' in mediafile or 'mkv' in mediafile:
                                bot.send_video(chat_id=chat_num_id, video=open(MEDIA_ROOT + mediafile, 'rb'),
                                               caption=text,
                                               parse_mode='HTML')
                                # print('video sent')
                            else:
                                bot.send_message(chat_id=chat_num_id, text=text, parse_mode='HTML')
                                # print('text sent')
                            m_id.append(message_id)
                            DataBase.update_chat_error(('', chat_reference.replace('@', 'https://t.me/')))
                        except:
                            # print(traceback.format_exc())
                            if '403' in traceback.format_exc():
                                DataBase.update_chat_error(
                                    ('Ошибка 403 Бот не являестся администратором группы(канала)',
                                     chat_reference.replace('@', 'https://t.me/')))

                for poll in polls:  # По всем одобренным сообщениям
                    poll_day = poll[0]
                    question = poll[1]
                    post_time = poll[2]
                    options = []
                    option_1 = poll[4]
                    if option_1: options.append(option_1)
                    option_2 = poll[5]
                    if option_2: options.append(option_2)
                    option_3 = poll[6]
                    if option_3: options.append(option_3)
                    option_4 = poll[7]
                    if option_4: options.append(option_4)
                    option_5 = poll[8]
                    if option_5: options.append(option_5)
                    option_6 = poll[9]
                    if option_6: options.append(option_6)
                    option_7 = poll[10]
                    if option_7: options.append(option_7)
                    option_8 = poll[11]
                    if option_8: options.append(option_8)
                    option_9 = poll[12]
                    if option_9: options.append(option_9)
                    option_10 = poll[13]
                    if option_10: options.append(option_10)
                    is_anonymous = poll[14]
                    message_id = poll[-1]
                    post_time_init = datetime.strptime(post_time, '%H:%M:%S').strftime('%H:%M')
                    server_time = datetime.strftime(datetime.now(), '%H:%M')
                    server_time_plus = datetime.strftime(datetime.now() + timedelta(minutes=3), '%H:%M')
                    if post_time_init >= datetime.now().strftime('%H:%M') \
                            and post_time_init < server_time_plus and poll_day == post_bot_day:
                        try:
                            bot.send_poll(
                                chat_id=chat_num_id,
                                question=question,
                                options=[x for x in options],
                                is_anonymous=bool(is_anonymous)
                            )
                            poll_id.append(message_id)
                            DataBase.update_chat_error(('', chat_reference.replace('@', 'https://t.me/')))
                        except:
                            # print(traceback.format_exc())
                            if '403' in traceback.format_exc():
                                DataBase.update_chat_error(
                                    ('Ошибка 403 Бот не являестся администратором группы(канала)',
                                     chat_reference.replace('@', 'https://t.me/')))
            # print('m_id', m_id)
            for _id in m_id:
                DataBase.update_message_is_sent((True, _id))
            for _id in poll_id:
                DataBase.update_poll_is_sent((True, _id))

            # Если нет постов и опросов, то сдвигаемся к следующей дате
            messages = DataBase.get_posts((False, post_bot_day))
            polls = DataBase.get_posts((False, post_bot_day))
            # print(messages)
            if not messages and not polls:
                new_start_date_bot = str(datetime.strptime(start_date_bot, '%Y-%m-%d')
                                         + timedelta(days=1)).split(' ')[0]
                new_post_bot_day = post_bot_day + 1
                #  Обновляем день у бота +1
                DataBase.update_bot_day((new_start_date_bot, new_post_bot_day))
                #  Обновляем день у чатов, у которых день такой же как у бота +1
                # DataBase.update_chat_day_all((new_post_bot_day, post_bot_day))


if __name__ == '__main__':
    try:
        while True:
            post()
            sleep(5)
            sys.exit(1)
    except KeyboardInterrupt:
        print('Post Failed')
        print(KeyboardInterrupt)
