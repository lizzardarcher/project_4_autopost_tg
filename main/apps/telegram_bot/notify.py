import asyncio
import logging
import sys
import traceback

from telebot import TeleBot, logger
from telebot.async_telebot import AsyncTeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from database import DataBase
from threading import Thread

from utils import djangoORM
from apps.home.models import MessageToSend, Bot, UserToMail

logging.basicConfig(filename='bots.log',
          filemode='w',
          level=logging.DEBUG,
          format='%(asctime)s - %(levelname)s - %(filename)s - %(lineno)d - %(message)s')

token = DataBase.get_bots()[0][0]
bots = DataBase.get_bots()


def start_markup():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(InlineKeyboardButton(text='Принять ✅', callback_data='accept'))
    markup.add(InlineKeyboardButton(text='Отклонить 🚫', callback_data='decline'))
    return markup


async def run_bot(bot):
    bot = AsyncTeleBot(bot[0])

    @bot.message_handler(commands=['start'])
    async def start_handler(message):
        if message.chat.type == 'private':
            await bot.send_message(chat_id=message.chat.id,
                                   text='Вы желаете подписаться на уведомления от нашего бота?',
                                   reply_markup=start_markup())

    @bot.message_handler(commands=['send'])
    async def send_handler(message):
        if message.chat.type == 'private' and message.chat.id in [5566146968, 47866482, 60547682]:

            def mailing(message):
                count = 0
                if message.content_type == 'text':
                    user_ids = DataBase.get_user_to_mail()
                    for user_id in user_ids:
                        try:
                            bot.send_message(chat_id=user_id[0], text=message.text)
                            count += 1
                        except:
                            print(traceback.format_exc())
                elif message.content_type == 'photo':

                    user_ids = DataBase.get_user_to_mail()
                    for user_id in user_ids:
                        try:
                            bot.send_photo(chat_id=user_id[0], photo=message.photo[0].file_id, caption=message.text)
                            count += 1
                        except:
                            print(traceback.format_exc())

                elif message.content_type == 'video':

                    user_ids = DataBase.get_user_to_mail()
                    for user_id in user_ids:
                        try:
                            bot.send_video(chat_id=user_id[0], video=message.video[0].file_id, caption=message.text)
                            count += 1
                        except:
                            print(traceback.format_exc())
                bot.send_message(chat_id=message.chat.id,
                                 text=f'Рассылка закончена. Сообщение отправлено {count} пользователям')

            msg = bot.reply_to(message, text='Введите сообщение, которое вы хотите отпавить '
                                             'всем пользователям бота:...')
            bot.register_next_step_handler(msg, mailing)

    @bot.callback_query_handler(func=lambda call: True)
    async def abbracadabra(call):
        if call.message.chat.type == 'private':
            await bot.delete_message(call.message.chat.id, call.message.id)
            if 'accept' in call.data:
                user_id = call.message.chat.id
                username = call.message.chat.username
                first_name = call.message.chat.first_name
                last_name = call.message.chat.last_name
                try:
                    try:
                        UserToMail.objects.get(id=user_id).delete()
                    except:
                        ...
                    UserToMail.objects.create(id=user_id, username=username or '---',
                                              first_name=first_name or '---', last_name=last_name or '---')
                except:
                    print(traceback.format_exc())
                await bot.send_message(call.message.chat.id, 'Подписка на уведомления активирована ✅')
                await bot.send_message(call.message.chat.id,
                                       'Если хотите изменить подписку, запустите бота заново с помощью команды /start')
            if 'decline' in call.data:
                user_id = call.message.chat.id
                try:
                    UserToMail.objects.get(id=user_id).delete()
                except:
                    print(traceback.format_exc())
                await bot.send_message(call.message.chat.id, 'Подписка на уведомления отклонена 🚫')
                await bot.send_message(call.message.chat.id,
                                       'Если хотите изменить подписку, запустите бота заново с помощью команды /start')


    # @bot.message_handler(content_types=['new_chat_members'])
    # async def welcome_new_member(message):
    #     # bot.send_message(message.chat.id, 'всем чмоки в этом чатике')
    #     # print(message.json['new_chat_participant']['is_bot'])
    #     # print(type(message.json['new_chat_participant']['is_bot']))
    #     if message.json['new_chat_participant']['is_bot']:
    #         # bot.send_message(message.chat.id, 'всем чмоки в этом чатике')
    #         chat_id = message.json['chat']['id']
    #         print(chat_id)
    #         chat_title = message.json['chat']['title']
    #         DataBase.update_chat_id((chat_id, chat_title))
    #         print(chat_id, chat_title)

    @bot.message_handler(content_types=['new_chat_members'])
    async def handle_new_chat_member(message):
        try:
            chat_id = message.chat.id
            chat = await  bot.get_chat(chat_id)
            chat_title = chat.title
            DataBase.update_chat_id((chat_id, chat_title))
        except:
            logger.error(traceback.format_exc())

    await bot.infinity_polling(allowed_updates=['message', 'callback_query'])


async def run_bots():
    tasks = []
    for bot in bots:
        tasks.append(asyncio.create_task(run_bot(bot)))

    await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(run_bots())