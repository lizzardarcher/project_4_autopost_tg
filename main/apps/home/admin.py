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
    inlines = (UserSettingsInline,)




admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Bot)
# admin.site.register(UserSettings)
admin.site.register(UserToMail)
admin.site.register(Post)
admin.site.register(Poll)
admin.site.register(MessageToSend)
admin.site.site_url = "/bot"

# @admin.action(description="Mark selected stories as published")
# def make_bot(modeladmin, request, queryset):
#     queryset.update(bot=Bot.objects.get(pk=1))

# @admin.register(Post)
# class PostAdmin(admin.ModelAdmin):
#     actions = [make_bot]

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    # actions = [make_bot]
    ...