from .models import *


def user_settings(request):

    try:
        settings = UserSettings.objects.filter(user_id=request.user.id)[0]
    except IndexError:
        settings = None

    try:
        is_running = Bot.objects.get(id=1).is_started
        day = Bot.objects.get(id=1).day
    except IndexError:
        is_running = None
        day = None

    return {
        'settings': settings,
        'is_running': is_running,
        'day': day,
    }
