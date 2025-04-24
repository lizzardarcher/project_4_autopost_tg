import logging
import logging.handlers
import traceback
from time import sleep
from datetime import date, datetime, timedelta

from telebot import TeleBot, apihelper

from utils import djangoORM
from apps.home.models import Post, Bot, Chat, Poll

LOG_FILENAME = 'log.log'
LOG_LEVEL = logging.WARNING
LOG_MAX_BYTES = 10 * 1024 * 1024
LOG_BACKUP_COUNT = 5
logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)
handler = logging.handlers.RotatingFileHandler(
    LOG_FILENAME,
    maxBytes=LOG_MAX_BYTES,
    backupCount=LOG_BACKUP_COUNT,
    encoding='utf8'
)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

MEDIA_ROOT = '/var/www/html/main/core/static/media/'


def send_telegram_message(bot, chat_id, text=None, mediafile=None):
    """Отправляет сообщение в Telegram чат, обрабатывая различные типы медиа."""
    try:
        if mediafile:
            with open(MEDIA_ROOT + mediafile, 'rb') as f:
                if 'jpg' in mediafile or 'jpeg' in mediafile:
                    bot.send_photo(chat_id=chat_id, photo=f, caption=text, parse_mode='HTML')
                elif 'mp3' in mediafile:
                    bot.send_audio(chat_id=chat_id, audio=f, caption=text, parse_mode='HTML')
                elif 'mp4' in mediafile or 'mpeg' in mediafile or 'avi' in mediafile or 'mkv' in mediafile:
                    bot.send_video(chat_id=chat_id, video=f, caption=text, parse_mode='HTML')
        else:
            bot.send_message(chat_id=chat_id, text=text, parse_mode='HTML')
        return True
    except apihelper.ApiException as e:
        logger.error(f"Telegram API error: {e} Chat ID: {chat_id}")
        logger.error(traceback.format_exc())
        if '403' in str(e):
            logger.warning(f"Bot is not an administrator in chat {chat_id}")
            return False  # Indicate failure
        return False  # Indicate failure

    except FileNotFoundError:
        logger.error(f"Media file not found: {MEDIA_ROOT + mediafile}")
        return False  # Indicate failure

    except Exception as e:
        logger.error(f"General error sending message: {e} Chat ID: {chat_id}")
        logger.error(traceback.format_exc())
        return False  # Indicate failure


def send_telegram_poll(bot, chat_id, question, options, is_anonymous):
    """Отправляет опрос в Telegram чат."""
    try:
        # Remove None or empty strings from options
        valid_options = [opt for opt in options if opt]
        bot.send_poll(
            chat_id=chat_id,
            question=question,
            options=valid_options,
            is_anonymous=is_anonymous
        )
        return True
    except apihelper.ApiException as e:
        logger.error(f"Telegram API error sending poll: {e} Chat ID: {chat_id}")
        logger.error(traceback.format_exc())
        if '403' in str(e):
            logger.warning(f"Bot is not an administrator in chat {chat_id}")
        return False  # Indicate failure

    except Exception as e:
        logger.error(f"General error sending poll: {e} Chat ID: {chat_id}")
        logger.error(traceback.format_exc())
        return False  # Indicate failure


def process_bot(b):
    """Обрабатывает одного бота, отправляя сообщения и опросы."""
    bot = TeleBot(token=b.token)
    start_date_bot = b.start_date
    is_start_date_bot = start_date_bot == date.today()
    is_bot_active = b.is_started
    post_bot_day = b.day

    if is_start_date_bot and is_bot_active:
        chats = Chat.objects.filter(bot=b)
        messages = Post.objects.filter(is_sent=False, day=post_bot_day, bot=b)
        polls = Poll.objects.filter(is_sent=False, day=post_bot_day, bot=b)

        for chat in chats:
            chat_id = chat.chat_id if hasattr(chat, 'chat_id') and chat.chat_id else chat.reference  # Get chat ID safely

            # Process messages
            for message in messages:
                post_time = datetime.strptime(message.post_time.__str__(), '%H:%M:%S').strftime('%H:%M')
                server_time_plus = datetime.strftime(datetime.now() + timedelta(minutes=3), '%H:%M')

                if post_time >= datetime.now().strftime('%H:%M') and post_time < server_time_plus and message.day == post_bot_day:
                    if send_telegram_message(bot, chat_id, message.text, message.media_file.name if message.media_file else None):
                        Post.objects.filter(id=message.id).update(is_sent=True)
                        chat.error = ''
                        chat.save()
                    else:
                        chat.error = 'Failed to send message. See logs.'
                        chat.save()

            # Process polls
            for poll in polls:
                post_time = poll.post_time.strftime('%H:%M')  # Directly format datetime object

                server_time_plus = datetime.strftime(datetime.now() + timedelta(minutes=3), '%H:%M')

                if post_time >= datetime.now().strftime('%H:%M') and post_time < server_time_plus and poll.day == post_bot_day:
                    options = [poll.option_1, poll.option_2, poll.option_3, poll.option_4,
                               poll.option_5, poll.option_6, poll.option_7, poll.option_8,
                               poll.option_9, poll.option_10]
                    if send_telegram_poll(bot, chat_id, poll.question, options, poll.is_anonymous):
                        Poll.objects.filter(id=poll.id).update(is_sent=True)
                        chat.error = ''
                        chat.save()
                    else:
                        chat.error = 'Failed to send poll. See logs.'
                        chat.save()


def post():
    """Основная функция для обработки ботов и отправки контента."""
    bots = Bot.objects.all()
    for bot in bots:
        process_bot(bot)

    for b in Bot.objects.all():

        start_date_bot = b.start_date
        post_bot_day = b.day

        messages = Post.objects.filter(is_sent=False, day=post_bot_day, bot=b)
        polls = Poll.objects.filter(is_sent=False, day=post_bot_day, bot=b)

        if not messages.exists() and not polls.exists():  # Use .exists() for efficiency
            new_start_date_bot = start_date_bot + timedelta(days=1)
            new_post_bot_day = (post_bot_day % 7) + 1  # Cycle through days 1-7

            b.day = new_post_bot_day
            b.start_date = new_start_date_bot
            b.save()
            logger.info(f'Updating bot {b.id} to day {new_post_bot_day} and date {new_start_date_bot}')


if __name__ == '__main__':
    while True:
        try:
            post()
            sleep(5)
        except KeyboardInterrupt:
            print('Post script exiting.')
            break
