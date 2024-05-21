# -*- encoding: utf-8 -*-

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import *


class UserSettingsInline(admin.StackedInline):
    model = UserSettings
    can_delete = False
    verbose_name_plural = 'Настройки'


class UserAdmin(BaseUserAdmin):
    inlines = (UserSettingsInline, )

class ChatAdmin(admin.ModelAdmin):
    list_display = ('reference', 'title', 'chat_id')


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Bot)
admin.site.register(UserToMail)
admin.site.register(Post)
admin.site.register(Poll)
admin.site.register(Chat, ChatAdmin)
