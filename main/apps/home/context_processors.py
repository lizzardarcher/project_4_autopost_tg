from .models import *


# def user_settings(request):
#
#     try:
#         settings = UserSettings.objects.filter(user_id=request.user.id)[0]
#     except IndexError:
#         settings = None
#
#     try:
#         is_running = UserSettings.objects.filter(user_id=request.user.id)[0].bot_selected.is_started
#         day = UserSettings.objects.filter(user_id=request.user.id)[0].bot_selected.day
#     except IndexError:
#         is_running = None
#         day = None
#
#     try:
#         return {
#             'settings': settings,
#             'is_running': is_running,
#             'day': day,
#             'bot_name_1': Bot.objects.filter(id=1).first().title,
#             'bot_name_2': Bot.objects.filter(id=2).first().title,
#             'bot_name_3': Bot.objects.filter(id=3).first().title,
#             'bot_name_4': Bot.objects.filter(id=4).first().title,
#             'bot_name_5': Bot.objects.filter(id=7).first().title,
#             'bot_name_6': Bot.objects.filter(id=8).first().title,
#             'bot_name_7': Bot.objects.filter(id=10).first().title,
#             'bot_name_8': Bot.objects.filter(id=11).first().title,
#             # 'bot_name_9': Bot.objects.filter(id=12).first().title,
#             # 'bot_name_10': Bot.objects.filter(pk=13).first().title,
#             'bot_is_active_1': Bot.objects.filter(pk=1).first().is_started,
#             'bot_is_active_2': Bot.objects.filter(pk=2).first().is_started,
#             'bot_is_active_3': Bot.objects.filter(pk=3).first().is_started,
#             'bot_is_active_4': Bot.objects.filter(pk=4).first().is_started,
#             'bot_is_active_5': Bot.objects.filter(pk=7).first().is_started,
#             'bot_is_active_6': Bot.objects.filter(pk=8).first().is_started,
#             'bot_is_active_7': Bot.objects.filter(pk=10).first().is_started,
#             'bot_is_active_8': Bot.objects.filter(pk=11).first().is_started,
#             # 'bot_is_active_9': Bot.objects.filter(pk=12).first().is_started,
#             # 'bot_is_active_10': Bot.objects.filter(pk=13).first().is_started,
#             'bot_selected': UserSettings.objects.filter(user_id=request.user.id)[0].bot_selected,
#         }
#     except:
#         return {
#             'settings': settings,
#         }


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


