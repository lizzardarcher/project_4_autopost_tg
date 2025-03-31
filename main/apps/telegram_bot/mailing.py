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
    except Exception:
        pass


async def post():
    bots = Bot.objects.all()
    messages = MessageToNotify.objects.all()
    users = UserToMail.objects.all()
    # users = UserToMail.objects.all().filter(id=5566146968)
    weekday = datetime.now().weekday()
    current_time = datetime.now().strftime('%H:%M')

    async def process_bot(bot_obj):
        bot = AsyncTeleBot(bot_obj.token)
        for message in messages:
            days_to_send = [message.day_to_send_1, message.day_to_send_2, message.day_to_send_3,
                            message.day_to_send_4, message.day_to_send_5, message.day_to_send_6,
                            message.day_to_send_7]
            if any(day and weekday == WEEKDAYS[day] for day in days_to_send):
                if current_time == message.time_to_send.strftime('%H:%M'):
                    tasks = [send_message_safe(bot, user.id, message.message) for user in users]
                    await asyncio.gather(*tasks)
                    await asyncio.sleep(60)

    bot_tasks = [process_bot(bot) for bot in bots]
    await asyncio.gather(*bot_tasks)


async def main():
    while True:
        try:
            await post()
            await asyncio.sleep(1)
        except KeyboardInterrupt:
            print(KeyboardInterrupt)
            break


if __name__ == "__main__":
    asyncio.run(main())
