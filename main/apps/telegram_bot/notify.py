from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from database import DataBase

token = DataBase.get_bot()[0]
bot = TeleBot(token)


def start_markup():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(InlineKeyboardButton(text='Принять ✅', callback_data='accept'))
    markup.add(InlineKeyboardButton(text='Отклонить 🚫', callback_data='decline'))
    return markup


@bot.message_handler(commands=['start'])
def start_handler(message):
    if message.chat.type == 'private':
        bot.send_message(chat_id=message.chat.id, text='Вы желаете подписаться на уведомления от нашего бота?',
                         reply_markup=start_markup())


@bot.message_handler(commands=['send'])
def send_handler(message):
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
                        bot.send_video(chat_id=user_id[0], photo=message.video[0].file_id, caption=message.text)
                        count += 1
                    except:
                        print(traceback.format_exc())
            bot.send_message(chat_id=message.chat.id,
                             text=f'Рассылка закончена. Сообщение отправлено {count} пользователям')

        msg = bot.reply_to(message, text='Введите сообщение, которое вы хотите отпавить '
                                         'всем пользователям бота:...')
        bot.register_next_step_handler(msg, mailing)


@bot.callback_query_handler(func=lambda call: True)
def abbracadabra(call):
    if call.message.chat.type == 'private':
        bot.delete_message(call.message.chat.id, call.message.id)
        if 'accept' in call.data:
            user_id = call.message.from_user.id
            DataBase.set_user_to_mail(int(user_id))
            print('User set: ', user_id)
            bot.send_message(call.message.chat.id, 'Подписка на уведомления активирована ✅')
            bot.send_message(call.message.chat.id,
                             'Если хотите изменить подписку, запустите бота заново с помощью команды /start')
        if 'decline' in call.data:
            user_id = call.message.from_user.id
            DataBase.delete_user_to_mail(int(user_id))
            print('User deleted: ', user_id)
            bot.send_message(call.message.chat.id, 'Подписка на уведомления отклонена 🚫')
            bot.send_message(call.message.chat.id,
                             'Если хотите изменить подписку, запустите бота заново с помощью команды /start')


@bot.message_handler(content_types=['new_chat_members'])
def welcome_new_member(message):
    # bot.send_message(message.chat.id, 'всем чмоки в этом чатике')
    # print(message.json['new_chat_participant']['is_bot'])
    # print(type(message.json['new_chat_participant']['is_bot']))
    if message.json['new_chat_participant']['is_bot']:
        # bot.send_message(message.chat.id, 'всем чмоки в этом чатике')
        chat_id = message.json['chat']['id']
        print(chat_id)
        chat_title = message.json['chat']['title']
        DataBase.update_chat_id((chat_id, chat_title))
        print(chat_id, chat_title)


bot.infinity_polling(allowed_updates=['message', 'callback_query'])
