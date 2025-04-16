import asyncio
from datetime import datetime
from telebot.async_telebot import AsyncTeleBot

from utils import djangoORM
from apps.home.models import MessageToNotify, Bot, UserToMail

WEEKDAYS = {
    'Понедельник': 0,
    'Вторник': 1,
    'Среда': 2,
    'Четверг': 3,
    'Пятница': 4,
    'Суббота': 5,
    'Воскресенье': 6,
}


async def send_message_safe(bot, chat_id, text):
    """
    Asynchronous wrapper for sending messages, handles exceptions.
    """
    try:
        await bot.send_message(chat_id=chat_id, text=text)
    except Exception as e:
        print(f"Error sending message to {chat_id}: {e}")


async def post():
    try:
        users = list(UserToMail.objects.all())
        weekday = datetime.now().weekday()
        current_time = datetime.now().strftime('%H:%M')

        async def process_message(message):
            try:
                bot_obj = message.bot
                bot = AsyncTeleBot(bot_obj.token)

                days_to_send = [message.day_to_send_1, message.day_to_send_2, message.day_to_send_3,
                                message.day_to_send_4, message.day_to_send_5, message.day_to_send_6,
                                message.day_to_send_7]

                if any(day and weekday == WEEKDAYS[day] for day in days_to_send):
                    message_time = message.time_to_send.strftime('%H:%M')
                    if current_time == message_time:
                        tasks = [send_message_safe(bot, user.id, message.message) for user in users]
                        await asyncio.gather(*tasks)

            except Exception as e:
                print(f"Error processing message {message.id}: {e}")

        messages_to_send = []
        for message in MessageToNotify.objects.all():
            days_to_send = [message.day_to_send_1, message.day_to_send_2, message.day_to_send_3,
                            message.day_to_send_4, message.day_to_send_5, message.day_to_send_6,
                            message.day_to_send_7]
            if any(day and weekday == WEEKDAYS[day] for day in days_to_send):
                message_time = message.time_to_send.strftime('%H:%M')
                if current_time == message_time:
                    messages_to_send.append(message)

        message_tasks = [process_message(message) for message in messages_to_send]  # Create task for each message
        await asyncio.gather(*message_tasks)

    except Exception as e:
        print(f"Error in post function: {e}")


async def main():
    while True:
        try:
            await post()
            await asyncio.sleep(60)
        except KeyboardInterrupt:
            print("KeyboardInterrupt")
            break
        except Exception as e:
            print(f"Unhandled error in main loop: {e}")
            await asyncio.sleep(60)


if __name__ == "__main__":
    asyncio.run(main())
