import logging.handlers
import traceback
from time import sleep
from datetime import date, datetime, timedelta

from telebot import TeleBot, apihelper

from utils import djangoORM
from apps.home.models import Post, Bot, Chat, Poll

LOG_FILENAME = 'log.log'
LOG_LEVEL = logging.INFO
LOG_MAX_BYTES = 10 * 1024 * 1024
LOG_BACKUP_COUNT = 5
logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)
handler = logging.handlers.RotatingFileHandler(
    LOG_FILENAME,
    maxBytes=LOG_MAX_BYTES,
    backupCount=LOG_BACKUP_COUNT,
    encoding='utf-8'
)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

MEDIA_ROOT = '/var/www/html/main/core/static/media/'


def send_telegram_message(bot, chat_id, text=None, mediafile=None):
    """Отправляет сообщение в Telegram чат, обрабатывая различные типы медиа."""
    try:
        if mediafile:
            full_media_path = MEDIA_ROOT + mediafile
            if text is None:
                text = '*************************'
            logger.info(f"Sending media file: {full_media_path}")

            with open(full_media_path, 'rb') as f:
                if 'jpg' in mediafile.lower() or 'jpeg' in mediafile.lower() or 'png' in mediafile.lower():
                    logger.info(f"Sending photo with caption: {text}")
                    bot.send_photo(chat_id=chat_id, photo=f, caption=text, parse_mode='HTML')
                elif 'mp3' in mediafile.lower():
                    logger.info(f"Sending audio with caption: {text}")
                    bot.send_audio(chat_id=chat_id, audio=f, caption=text, parse_mode='HTML')
                elif 'mp4' in mediafile.lower() or 'mpeg' in mediafile.lower() or 'avi' in mediafile.lower() or 'mkv' in mediafile.lower():
                    logger.info(f"Sending video with caption: {text}")
                    bot.send_video(chat_id=chat_id, video=f, caption=text, parse_mode='HTML')
                else:
                    logger.warning(f"Unsupported media file type: {mediafile}")
                    return False
        else:
            logger.info(f"Sending text message: {text}")
            bot.send_message(chat_id=chat_id, text=text, parse_mode='HTML')


        logger.info(f"Successfully sent Telegram message to chat ID: {chat_id}")
        return True

    except apihelper.ApiException as e:
        logger.error(f"Telegram API error: {e} Chat ID: {chat_id} Bot ID: {Chat.objects.filter(chat_id=chat_id).first().bot.title}")
        send_telegram_alert(
            f"Ошибка отправки Telegram сообщения: {e} "
            f"Чат ID: {Chat.objects.filter(chat_id=chat_id).first()}"
            f"Бот ID: {Bot.objects.filter(chat_id=chat_id).first()}"
            f"Описание ошибки: {traceback.format_exc()}"
        )
        if '403' in str(e):
            logger.warning(f"Bot is not an administrator in chat {chat_id}")
            return False
        return False

    except FileNotFoundError:
        full_media_path = MEDIA_ROOT + mediafile if mediafile else "No media file specified"
        logger.error(f"Media file not found: {full_media_path}")
        return False  # Indicate failure

    except Exception as e:
        logger.error(f"General error sending message: {e} Chat ID: {chat_id}")
        return False  # Indicate failure


def send_telegram_poll(bot, chat_id, question, options, is_anonymous):
    """Отправляет опрос в Telegram чат."""
    try:
        logger.info(
            f"Attempting to send Telegram poll to chat ID: {chat_id}, Question: {question}, Options: {options}, Anonymous: {is_anonymous}")

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
        if '403' in str(e):
            logger.warning(f"Bot is not an administrator in chat {chat_id}")
        return False  # Indicate failure

    except Exception as e:
        logger.error(f"General error sending poll: {e} Chat ID: {chat_id}")
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
        messages = Post.objects.filter(is_sent=False, day=post_bot_day, bot=b, is_for_sched=False)
        polls = Poll.objects.filter(is_sent=False, day=post_bot_day, bot=b)

        for chat in chats:
            chat_id = chat.chat_id if hasattr(chat, 'chat_id') and chat.chat_id else chat.reference  # Get chat ID safely
            try:
                for message in messages:
                    try:
                        post_time = datetime.strptime(message.post_time.__str__(), '%H:%M:%S').strftime('%H:%M')
                    except Exception as e:
                        break
                    server_time_plus = datetime.strftime(datetime.now() + timedelta(minutes=3), '%H:%M')

                    if post_time >= datetime.now().strftime('%H:%M') and post_time < server_time_plus and message.day == post_bot_day:
                        logger.info(f"Bot {b.id}, Chat {chat_id}: Sending message ID {message.id} with text: {message.text[:50]}... (truncated)")
                        media_file_name = message.media_file.name if message.media_file else None
                        if send_telegram_message(bot, chat_id, message.text, media_file_name):
                            Post.objects.filter(id=message.id).update(is_sent=True)
                            chat.error = ''
                            chat.save()
                        else:
                            chat.error = 'Failed to send message. See logs.'
                            chat.save()

                    else:
                        ...
            except Exception as e:
                logger.error(f"Error processing message: {e}")
            # Process polls
            for poll in polls:
                post_time = poll.post_time.strftime('%H:%M')  # Directly format datetime object
                server_time_plus = datetime.strftime(datetime.now() + timedelta(minutes=3), '%H:%M')

                if post_time >= datetime.now().strftime(
                        '%H:%M') and post_time < server_time_plus and poll.day == post_bot_day:
                    logger.info(
                        f"Bot {b.id}, Chat {chat_id}: Sending poll ID {poll.id} with question: {poll.question[:50]}... (truncated)")
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

                else:
                    ...

def send_telegram_alert(message):
    """Отправляет сообщение в Telegram-чат."""
    token = '7773031484:AAFe0j5IDJq_O4l3Jr7KQEBOmGrvtmHs9SI'
    chat_id = -1002504453107

    bot_telegram = TeleBot(token=token)

    try:
        bot_telegram.send_message(chat_id=chat_id, text=message, parse_mode='HTML')
        logger.info(f"Telegram alert sent: {message}")
    except Exception as e:
        logger.error(f"Error sending Telegram alert: {e}")


def post():
    """Основная функция для обработки ботов и отправки контента."""
    bots = Bot.objects.filter(is_started=True)
    logger.info(f"Starting 'post' function. Found {bots.count()} bots to process.")

    for bot in bots:
        process_bot(bot)

    for b in bots:

        start_date_bot = b.start_date
        post_bot_day = b.day

        messages = Post.objects.filter(is_sent=False, day=post_bot_day, bot=b, is_for_sched=False)                      # Unsent messages for the current day
        polls = Poll.objects.filter(is_sent=False, day=post_bot_day, bot=b)                                             # Unsent polls for the current day

        # message of the last day
        messages_last_day = Post.objects.filter(bot=b, is_for_sched=False)
        days_list = []
        for m in messages_last_day:
            days_list.append(m.day)
        messages_last_day = max(days_list) if days_list else 0

        logger.debug(f"Bot {b.title}: Checking for scheduled day/date update. Messages: {messages.count()}, Polls: {polls.count()}")


        if not messages.exists() and not polls.exists():
            new_start_date_bot = start_date_bot + timedelta(days=1)

            if messages_last_day == post_bot_day and not Post.objects.filter(day=messages_last_day, is_sent=False, bot=b, is_for_sched=True).exists():
                b.day = 1
                b.is_started=False
            else:
                b.day = post_bot_day + 1
                b.start_date = new_start_date_bot

            b.save()

            logger.info(f'Updating bot {b.title} to day {post_bot_day + 1} and date {new_start_date_bot}')
        else:
            logger.debug(
                f"Bot {b.title}: Not updating day/date because messages or polls are still pending.")
    logger.info("Finished 'post' function.")


if __name__ == '__main__':
    logger.info("Starting main post script.")
    # send_telegram_alert(
    #     f"Скрипт для публикации контента запущен [<code>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</code>]\n\n"
    #     f"В базе данных находится:\n"
    #     f"Ботов: [<code>{Bot.objects.count()}</code>]\n"
    #     f"Групп: [<code>{Chat.objects.count()}</code>]\n"
    #     f"Cообщений: [<code>{Post.objects.count()}</code>]\n"
    #     f"Опросов: [<code>{Poll.objects.count()}</code>]."
    # )
    while True:
        try:
            post()
            sleep(5)
        except KeyboardInterrupt:
            logger.info('Post script exiting due to KeyboardInterrupt.')
            break
        except Exception as e:
            logger.error(f"An unhandled exception occurred in the main loop: {e}")
            send_telegram_alert(
                f"Скрипт для публикации контента завершил работу с ошибкой: {e}")
            logger.error(traceback.format_exc())
