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
        context['bot_list'] = Bot.objects.all()

    except UserSettings.DoesNotExist:
        context['settings'] = None
        context['is_running'] = None
        context['day'] = None
        context['bot_selected'] = None
        context['bot_list'] = None


    bot_ids = [x.id for x in Bot.objects.all()]

    for i, bot_id in enumerate(bot_ids):
        try:
            bot = Bot.objects.get(id=bot_id)
            context[f'bot_name_{i+1}'] = bot.title
            context[f'bot_is_active_{i+1}'] = bot.is_started
        except Bot.DoesNotExist:
            context[f'bot_name_{i+1}'] = None
            context[f'bot_is_active_{i+1}'] = None


    return context


