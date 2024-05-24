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

    try:
        return {
            'settings': settings,
            'is_running': is_running,
            'day': day,
            'bot_name_1': Bot.objects.get(pk=1).title,
            'bot_name_2': Bot.objects.get(pk=2).title,
            'bot_name_3': Bot.objects.get(pk=3).title,
            'bot_name_4': Bot.objects.get(pk=4).title,
            'bot_name_5': Bot.objects.get(pk=5).title,
            'bot_name_6': Bot.objects.get(pk=6).title,
            'bot_name_7': Bot.objects.get(pk=7).title,
            'bot_name_8': Bot.objects.get(pk=8).title,
            'bot_name_9': Bot.objects.get(pk=9).title,
            'bot_name_10': Bot.objects.get(pk=10).title,
            'bot_is_active_1': Bot.objects.get(pk=1).is_started,
            'bot_is_active_2': Bot.objects.get(pk=2).is_started,
            'bot_is_active_3': Bot.objects.get(pk=3).is_started,
            'bot_is_active_4': Bot.objects.get(pk=4).is_started,
            'bot_is_active_5': Bot.objects.get(pk=5).is_started,
            'bot_is_active_6': Bot.objects.get(pk=6).is_started,
            'bot_is_active_7': Bot.objects.get(pk=7).is_started,
            'bot_is_active_8': Bot.objects.get(pk=8).is_started,
            'bot_is_active_9': Bot.objects.get(pk=9).is_started,
            'bot_is_active_10': Bot.objects.get(pk=10).is_started,
            'bot_selected': UserSettings.objects.filter(user_id=request.user.id)[0].bot_selected,
        }
    except:
        return {
            'settings': settings,
        }
