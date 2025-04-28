from .models import *


def user_settings(request):
    """
    Возвращает словарь настроек пользователя для отображения в шаблоне.
    """
    user_id = request.user.id
    context = {}  # Initialize the context dictionary

    try:
        settings = UserSettings.objects.get(user_id=user_id)
        context['settings'] = settings
        context['is_running'] = settings.bot_selected.is_started
        context['day'] = settings.bot_selected.day
        context['bot_selected'] = settings.bot_selected

    except UserSettings.DoesNotExist:
        # Handle the case where UserSettings doesn't exist for the user
        context['settings'] = None
        context['is_running'] = None
        context['day'] = None
        context['bot_selected'] = None  # Or a default value if appropriate

    # Fetch bot information dynamically
    bot_ids = [1, 2, 3, 4, 7, 8, 10, 11]  # List of bot IDs
    for i, bot_id in enumerate(bot_ids):
        try:
            bot = Bot.objects.get(id=bot_id)
            context[f'bot_name_{i+1}'] = bot.title
            context[f'bot_is_active_{i+1}'] = bot.is_started
        except Bot.DoesNotExist:
            # Handle the case where a Bot doesn't exist for the given id
            context[f'bot_name_{i+1}'] = None
            context[f'bot_is_active_{i+1}'] = None


    return context


