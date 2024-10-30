# import os
# import django
# os.environ['DJANGO_SETTINGS_MODULE'] = 'core.settings'
# os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
# django.setup()
from apps.telegram_bot.utils import djangoORM
from apps.home.models import *
p = Post.objects.all()

print(p)