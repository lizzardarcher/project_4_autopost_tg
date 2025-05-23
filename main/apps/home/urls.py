# -*- encoding: utf-8 -*-

from django.urls import path, re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = [

    path('', views.ves_v_norme_redirect, name='ves_v_norme_redirect'),
    path('bot', views.index, name='home'),
    path('bot_list', views.BotListView.as_view(), name='bot_list'),

    path('bot_create', views.BotCreateView.as_view(), name='bot_create'),
    path('bot_delete/<int:pk>', views.BotDeleteView.as_view(), name='bot_delete'),

    path('update_post_is_sent', views.update_post_is_sent, name='update_post_is_sent'),
    path('user_profile_update/<int:pk>', views.UserSettingsUpdateView.as_view(), name='user update view'),
    path('user_profile/<int:pk>', views.UserUpdateView.as_view(), name='user profile'),

    path('chats', views.ChatListView.as_view(), name='Chat list view'),
    path('chat_create', views.ChatCreateView.as_view(), name='Chat create view'),
    path('chat_update/<int:pk>', views.ChatUpdateView.as_view(), name='Chat update view'),
    path('chat_delete/<int:pk>', views.ChatDeleteView.as_view(), name='Chat delete view'),

    path('posts', views.PostListView.as_view(), name='Post list view'),
    # path('posts/<int:pk>', views.PostByDayListView.as_view(), name='Post by day list view'),
    path('post_create', views.PostCreateView.as_view(), name='Post create view'),
    path('post_update/<int:pk>', views.PostUpdateView.as_view(), name='Post update view'),
    path('post_delete/<int:pk>', views.PostDeleteView.as_view(), name='Post delete view'),

    path('sched', views.PostForScheduleListView.as_view(), name='sched'),
    path('sched_create', views.PostForScheduleCreateView.as_view(), name='sched_create'),
    path('sched_update/<int:pk>', views.PostForScheduleUpdateView.as_view(), name='sched_update'),
    path('sched_delete/<int:pk>', views.PostForScheduleDeleteView.as_view(), name='sched_delete'),

    path('polls', views.PollListView.as_view(), name='Poll list view'),
    path('poll_create', views.PollCreateView.as_view(), name='Poll create view'),
    path('poll_update/<int:pk>', views.PollUpdateView.as_view(), name='Poll update view'),
    path('poll_delete/<int:pk>', views.PollDeleteView.as_view(), name='Poll delete view'),

    path('bot_update/<int:pk>', views.BotUpdateView.as_view(), name='bot_update'),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    path('change_bot_selected/<int:id>', views.change_bot_selected, name='Change bot selected'),

    path('notify', views.UserToMailListView.as_view(), name='notify'),
    path('message_to_notify_create', views.MessageToNotifyCreateView.as_view(), name='message_to_notify_create'),
    path('message_to_notify_update/<int:pk>', views.MessageToNotifyUpdateView.as_view(), name='message_to_notify_update'),
    path('message_to_notify_delete/<int:pk>', views.message_to_notify_delete, name='message_to_notify_delete'),
    path('user_to_notify_delete/<int:pk>', views.user_to_notify_delete, name='user_to_notify_delete'),
]

# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)