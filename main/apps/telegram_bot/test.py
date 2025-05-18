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
        logger.info(f"Attempting to send Telegram message to chat ID: {chat_id}")

        if mediafile:
            full_media_path = MEDIA_ROOT + mediafile
            logger.info(f"Sending media file: {full_media_path}")

            with open(full_media_path, 'rb') as f:
                if 'jpg' in mediafile or 'jpeg' in mediafile:
                    logger.info(f"Sending photo with caption: {text}")
                    bot.send_photo(chat_id=chat_id, photo=f, caption=text, parse_mode='HTML')
                elif 'mp3' in mediafile:
                    logger.info(f"Sending audio with caption: {text}")
                    bot.send_audio(chat_id=chat_id, audio=f, caption=text, parse_mode='HTML')
                elif 'mp4' in mediafile or 'mpeg' in mediafile or 'avi' in mediafile or 'mkv' in mediafile:
                    logger.info(f"Sending video with caption: {text}")
                    bot.send_video(chat_id=chat_id, video=f, caption=text, parse_mode='HTML')
                else:
                    logger.warning(f"Unsupported media file type: {mediafile}")
                    return False  # Indicate failure
        else:
            logger.info(f"Sending text message: {text}")
            bot.send_message(chat_id=chat_id, text=text, parse_mode='HTML')

        logger.info(f"Successfully sent Telegram message to chat ID: {chat_id}")
        return True

    except apihelper.ApiException as e:
        logger.error(f"Telegram API error: {e} Chat ID: {chat_id}")
        logger.error(traceback.format_exc())
        if '403' in str(e):
            logger.warning(f"Bot is not an administrator in chat {chat_id}")
            return False  # Indicate failure
        return False  # Indicate failure

    except FileNotFoundError:
        full_media_path = MEDIA_ROOT + mediafile if mediafile else "No media file specified"
        logger.error(f"Media file not found: {full_media_path}")
        return False  # Indicate failure

    except Exception as e:
        logger.error(f"General error sending message: {e} Chat ID: {chat_id}")
        logger.error(traceback.format_exc())
        return False  # Indicate failure


def send_telegram_poll(bot, chat_id, question, options, is_anonymous):
    """Отправляет опрос в Telegram чат."""
    try:
        logger.info(f"Attempting to send Telegram poll to chat ID: {chat_id}, Question: {question}, Options: {options}, Anonymous: {is_anonymous}")

        # Remove None or empty strings from options
        valid_options = [opt for opt in options if opt]

        if not valid_options:
            logger.warning("No valid options provided for the poll.  Aborting sending poll.")
            return False

        logger.info(f"Sending poll with valid options: {valid_options}")

        bot.send_poll(
            chat_id=chat_id,
            question=question,
            options=valid_options,
            is_anonymous=is_anonymous
        )

        logger.info(f"Successfully sent Telegram poll to chat ID: {chat_id}")
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
    logger.info(f"Processing bot: {b.id}, Token: {b.token[:5]}... (truncated)") # Log bot ID and truncated token
    bot = TeleBot(token=b.token)
    chat = Chat.objects.filter(bot=b, chat_id=-1002664253448).first()
    message = Post.objects.filter(id=74).first()
    logger.info(f"Bot {b.id}: Found {chat} chats, {message} message,")
    media_file_name = message.media_file.name if message.media_file else None
    if send_telegram_message(bot, chat.chat_id, message.text, media_file_name):
        Post.objects.filter(id=message.id).update(is_sent=True)
        chat.error = ''
        chat.save()
        logger.info(f"Bot {b.id}, Chat {chat.chat_id}: Successfully sent message ID {message.id}")
    else:
        chat.error = 'Failed to send message. See logs.'
        chat.save()
        logger.error(f"Bot {b.id}, Chat {chat.chat_id}: Failed to send message ID {message.id}. See logs.")



def post():
    """Основная функция для обработки ботов и отправки контента."""
    bots = Bot.objects.all()
    logger.info(f"Starting 'post' function.  Found {bots.count()} bots to process.")

    for bot in bots:
        process_bot(bot)

    for b in Bot.objects.all(): # Re-query bots in case process_bot modified them.  Important for persistence.

        start_date_bot = b.start_date
        post_bot_day = b.day

        messages = Post.objects.filter(is_sent=False, day=post_bot_day, bot=b)
        polls = Poll.objects.filter(is_sent=False, day=post_bot_day, bot=b)

        logger.debug(f"Bot {b.id}: Checking for scheduled day/date update. Messages: {messages.count()}, Polls: {polls.count()}")

        if not messages.exists() and not polls.exists():  # Use .exists() for efficiency
            new_start_date_bot = start_date_bot + timedelta(days=1)
            new_post_bot_day = (post_bot_day % 7) + 1  # Cycle through days 1-7

            b.day = new_post_bot_day
            b.start_date = new_start_date_bot
            b.save()
            logger.info(f'Updating bot {b.id} to day {new_post_bot_day} and date {new_start_date_bot}')
        else:
            logger.debug(f"Bot {b.id}: Not updating day/date because messages or polls are still pending.")

    logger.info("Finished 'post' function.")


if __name__ == '__main__':
    logger.info("Starting main post script.")
    while True:
        try:
            post()
            sleep(5)
        except KeyboardInterrupt:
            logger.info('Post script exiting due to KeyboardInterrupt.')
            print('Post script exiting.')
            break
        except Exception as e:
            logger.error(f"An unhandled exception occurred in the main loop: {e}")
            logger.error(traceback.format_exc())
            # Consider adding a delay here or exiting after a certain number of errors.