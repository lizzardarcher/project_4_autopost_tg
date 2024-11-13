from utils import djangoORM
from apps.home.models import Post, Bot, Chat, Poll

import traceback
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
    # bots = DataBase.get_bots()
    bots = Bot.objects.all()
    for b in bots:
        bot = TeleBot(token=b.token)

        start_date_bot = b.start_date  # дата старта бота

        is_start_date_bot = start_date_bot == date.today() # совпадает ли дата старта с сегодняшней

        is_bot_active = b.is_started  # активен ли бот

        post_bot_day = b.day  # день постинга у бота

        if is_start_date_bot and is_bot_active:
            chats = Chat.objects.filter(bot=b) # Все чаты

            # Посты. Неотправленные и у которых день постинга совпадает с днём у бота
            messages = Post.objects.filter(is_sent=False, day=post_bot_day, bot=b)

            # Опрос. Неотправленные и у которых день постинга совпадает с днём у бота
            polls = Poll.objects.filter(is_sent=False, day=post_bot_day, bot=b)

            m_id = []
            poll_id = []
            for chat in chats:  # По всем чатам
                chat_reference = chat.reference
                try:
                    chat_num_id = chat.chat_id
                except:
                    chat_num_id = chat_reference

                for message in messages:  # По всем одобренным сообщениям
                    message_day = message.day
                    text = message.text
                    mediafile = message.media_file.name
                    post_time = message.post_time
                    message_id = message.id
                    post_time_init = datetime.strptime(post_time.__str__(), '%H:%M:%S').strftime('%H:%M')
                    server_time = datetime.strftime(datetime.now(), '%H:%M')
                    server_time_plus = datetime.strftime(datetime.now() + timedelta(minutes=3), '%H:%M')
                    # if datetime.strptime(post_time, '%H:%M:%S').strftime('%H:%M') == datetime.now().strftime('%H:%M') and message_day == post_bot_day:
                    # print(f"[Post time : {post_time_init}] [Time now() {datetime.now().strftime('%H:%M')}] [Time now() + {server_time_plus}]")
                    # print(f"[Start time : {post_time_init >= datetime.now().strftime('%H:%M')}]")
                    # print(f"[Time start < server_time_plus : {post_time_init < server_time_plus}]")
                    # print(f"[Message day`n bot_day  {message_day}] / [{post_bot_day}] [{message_day == post_bot_day}]")

                    if post_time_init >= datetime.now().strftime('%H:%M') and post_time_init < server_time_plus and message_day == post_bot_day:
                        try:
                            print('Posting accepted', message_id)
                            if 'jpg' in mediafile or 'jpeg' in mediafile:
                                bot.send_photo(chat_id=chat_num_id, photo=open(MEDIA_ROOT + mediafile, 'rb'),
                                               caption=text,
                                               parse_mode='HTML')
                                print('Photo sent')
                            elif 'mp3' in mediafile:
                                bot.send_audio(chat_id=chat_num_id, audio=open(MEDIA_ROOT + mediafile, 'rb'),
                                               caption=text,
                                               parse_mode='HTML')
                                print('audio sent')
                            elif 'mp4' in mediafile or 'mpeg' in mediafile or 'avi' in mediafile or 'mkv' in mediafile:
                                bot.send_video(chat_id=chat_num_id, video=open(MEDIA_ROOT + mediafile, 'rb'),
                                               caption=text,
                                               parse_mode='HTML')
                                print('video sent')
                            else:
                                bot.send_message(chat_id=chat_num_id, text=text, parse_mode='HTML')
                                print('text sent')
                            m_id.append(message_id)
                            chat.error = ''
                            chat.save()
                            Post.objects.filter(id=message_id).update(is_sent=True)
                            # DataBase.update_chat_error(('', chat_reference.replace('@', 'https://t.me/')))
                        except:
                            print(traceback.format_exc())
                            if '403' in traceback.format_exc():
                                chat.error = 'Ошибка 403 Бот не являестся администратором группы(канала)'
                                chat.save()
                                # DataBase.update_chat_error(('Ошибка 403 Бот не является администратором группы(канала)',chat_reference.replace('@', 'https://t.me/')))
                for poll in polls:  # По всем одобренным сообщениям
                    poll_day = poll.day
                    question = poll.question
                    post_time = poll.post_time
                    options = []
                    option_1 = poll.option_1
                    if option_1: options.append(option_1)
                    option_2 = poll.option_2
                    if option_2: options.append(option_2)
                    option_3 = poll.option_3
                    if option_3: options.append(option_3)
                    option_4 = poll.option_4
                    if option_4: options.append(option_4)
                    option_5 = poll.option_5
                    if option_5: options.append(option_5)
                    option_6 = poll.option_6
                    if option_6: options.append(option_6)
                    option_7 = poll.option_7
                    if option_7: options.append(option_7)
                    option_8 = poll.option_8
                    if option_8: options.append(option_8)
                    option_9 = poll.option_9
                    if option_9: options.append(option_9)
                    option_10 = poll.option_10
                    if option_10: options.append(option_10)
                    is_anonymous = poll.is_anonymous
                    message_id = poll.id
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
                            chat.error = ''
                            chat.save()
                            Poll.objects.filter(id=message_id).update(is_sent=True)
                            # DataBase.update_chat_error(('', chat_reference.replace('@', 'https://t.me/')))
                        except:
                            if '403' in traceback.format_exc():
                                chat.error = 'Ошибка 403 Бот не являестся администратором группы(канала)'
                                chat.save()
                                # DataBase.update_chat_error(('Ошибка 403 Бот не являестся администратором группы(канала)', chat_reference.replace('@', 'https://t.me/')))
            # print('m_id', m_id)
            # for _id in m_id:
            #     Post.objects.filter(id=_id).update(is_sent=True)
            #     # DataBase.update_message_is_sent((True, _id))
            # for _id in poll_id:
            #     Poll.objects.filter(id=_id).update(is_sent=True)
                # DataBase.update_poll_is_sent((True, _id))

            # Если нет постов и опросов, то сдвигаемся к следующей дате

            # messages = DataBase.get_posts((False, post_bot_day))

            messages = Post.objects.filter(is_sent=False, day=post_bot_day)

            # polls = DataBase.get_posts((False, post_bot_day))

            polls = Post.objects.filter(is_sent=False, day=post_bot_day)

            # print(messages, polls)

            if not messages and not polls:
                new_start_date_bot = str(datetime.strptime(start_date_bot, '%Y-%m-%d')
                                         + timedelta(days=1)).split(' ')[0]
                new_post_bot_day = post_bot_day + 1

                #  Обновляем день у бота +1

                b.day = new_post_bot_day
                b.start_date = new_start_date_bot
                b.save()

                # DataBase.update_bot_day((new_start_date_bot, new_post_bot_day, bot_id))
                #  Обновляем день у чатов, у которых день такой же как у бота +1
                # DataBase.update_chat_day_all((new_post_bot_day, post_bot_day))

# post()
if __name__ == '__main__':
    try:
        while True:
            # print('[PENDING] [...]')
            post()
            sleep(5)
            # sys.exit(1)
    except KeyboardInterrupt:
        print('Post Exit')
        print(KeyboardInterrupt)
