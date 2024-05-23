from .models import *


def user_settings(request):

    try:
        settings = UserSettings.objects.filter(user_id=request.user.id)[0]
    except IndexError:
        settings = None

    try:
        # is_running = Bot.objects.get(id=1).is_started
        # day = Bot.objects.get(id=1).day
        is_running = UserSettings.objects.filter(user_id=request.user.id)[0].bot_selected.is_started
        day = UserSettings.objects.filter(user_id=request.user.id)[0].bot_selected.day
    except IndexError:
        is_running = None
        day = None

    return {
        'settings': settings,
        'is_running': is_running,
        'day': day,
        'bot_name_1': Bot.objects.get(pk=1).title,
        'bot_name_2': Bot.objects.get(pk=2).title,
        'bot_selected': UserSettings.objects.filter(user_id=request.user.id)[0].bot_selected
    }
