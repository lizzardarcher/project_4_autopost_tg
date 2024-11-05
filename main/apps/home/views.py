# -*- encoding: utf-8 -*-
import math
from datetime import datetime
import os

from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.http import HttpResponse
from django.template import loader
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (ListView, DeleteView, UpdateView, CreateView, TemplateView, DetailView)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.forms import modelformset_factory
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.db import transaction

from .utils import get_chat_info
from .models import *
from .forms import *
from ..middleware import current_user


class UserView(SuccessMessageMixin, LoginRequiredMixin, TemplateView):
    model = User
    template_name = 'home/user_profile.html'


class UserUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    template_name = 'home/user_profile.html'
    model = User
    fields = ['username', 'email']
    success_url = '/user_profile'
    extra_context = {'segment': 'user'}
    success_message = 'Обновлено успешно!'

    def get_context_data(self, **kwargs):
        context = super(UserUpdateView, self).get_context_data(**kwargs)
        context.update({
            'settings': UserSettings.objects.filter(user=self.request.user)[0],
        })
        return context

    def form_valid(self, form):
        self.success_url = f'/user_profile/{form.instance.id}'
        return super().form_valid(form)


class UserSettingsUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = UserSettings
    template_name = 'crud/user_profile_update.html'
    form_class = UserSettingsForm
    success_url = '/'
    success_message = 'Обновлено успешно!'

    def form_valid(self, form):
        self.success_url = f'/user_profile/{form.instance.user.id}'
        return super().form_valid(form)


# CHATS #####################################################################

class ChatListView(SuccessMessageMixin, LoginRequiredMixin, ListView):
    extra_context = {'segment': 'chat'}
    model = Chat
    # paginate_by = 50
    template_name = 'home/chat_list.html'
    context_object_name = 'chats'

    def get_queryset(self):
        qs = self.model.objects.filter(
            bot=UserSettings.objects.get(user=self.request.user).bot_selected).order_by('-id')
        return qs


class ChatCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Chat
    template_name = 'crud/chat_create.html'
    form_class = ChatForm
    success_url = '/chats'
    success_message = 'Чат успешно добавлен!'

    def form_valid(self, form):
        form.instance.user = self.request.user

        # Парсим данные чата с помощью requests
        chat_data = get_chat_info(form.instance.reference)
        form.instance.title = chat_data[1]
        if 'data:image' in chat_data[0]:
            form.instance.image = chat_data[0]
        else:
            form.instance.image_url = chat_data[0]
        return super().form_valid(form)


class ChatUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Chat
    template_name = 'crud/chat_create.html'
    form_class = ChatForm
    success_url = '/chats'
    success_message = 'Чат успешно обновлён!'


class ChatDeleteView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = Chat
    success_url = '/chats'
    template_name = 'crud/chat_delete.html'
    success_message = 'Чат успешно Удалён!'


# POSTS #####################################################################

class PostListView(SuccessMessageMixin, LoginRequiredMixin, ListView):
    extra_context = {'segment': 'post'}
    model = Post
    paginate_by = 60
    template_name = 'home/post_list.html'
    context_object_name = 'posts'
    success_message = 'Пост успешно создан!'

    def get_queryset(self):
        qs = self.model.objects.filter(
            bot=UserSettings.objects.get(user=self.request.user).bot_selected, is_for_sched=False).order_by('day', 'post_time')
        return qs


# class PostByDayListView(SuccessMessageMixin, LoginRequiredMixin, ListView):
#     extra_context = {'segment': 'post'}
#     model = Post.objects.filter(day=pk)
#     print(model)
#     paginate_by = 25
#     template_name = 'home/post_list.html'
#     context_object_name = 'posts'
#     success_message = 'Пост успешно создан!'
#
#     def get_ordering(self, **kwargs):
#         ordering = self.request.GET.get('ordering', '-day')
#         return ordering


class PostCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    extra_context = {'segment': 'post'}
    model = Post
    template_name = 'crud/post_create.html'
    form_class = PostForm
    success_message = 'Пост успешно добавлен!'

    def get_success_url(self):
        res = '/posts'
        if 'page' in self.request.GET:
            res += f"?page={self.request.GET['page']}"
        return res


class PostUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    extra_context = {'segment': 'post'}
    model = Post
    template_name = 'crud/post_create.html'
    form_class = PostForm
    success_message = 'Пост успешно обновлён!'

    def get_success_url(self):
        res = '/posts'
        if 'page' in self.request.GET:
            res += f"?page={self.request.GET['page']}"
        return res


class PostDeleteView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    extra_context = {'segment': 'post'}
    model = Post
    success_url = '/posts'
    template_name = 'crud/post_delete.html'
    success_message = 'Пост успешно Удалён!'

# SCHEDULE #####################################################################

class PostForScheduleListView(SuccessMessageMixin, LoginRequiredMixin, ListView):
    extra_context = {'segment': 'sched'}
    model = Post
    paginate_by = 60
    template_name = 'home/post_for_sched.html'
    context_object_name = 'posts'
    success_message = 'Пост успешно создан!'

    def get_queryset(self):
        qs = self.model.objects.filter(
            bot=UserSettings.objects.get(user=self.request.user).bot_selected, is_for_sched=True).order_by('sched_datetime')
        return qs


class PostForScheduleCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    extra_context = {'segment': 'sched'}
    model = Post
    template_name = 'crud/post_for_sched_create.html'
    form_class = PostForScheduleForm
    success_message = 'Пост успешно добавлен!'

    def get_success_url(self):
        res = '/sched'
        if 'page' in self.request.GET:
            res += f"?page={self.request.GET['page']}"
        return res


class PostForScheduleUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    extra_context = {'segment': 'sched'}
    model = Post
    template_name = 'crud/post_for_sched_create.html'
    form_class = PostForScheduleForm
    success_message = 'Пост успешно обновлён!'

    def get_success_url(self):
        res = '/sched'
        if 'page' in self.request.GET:
            res += f"?page={self.request.GET['page']}"
        return res


class PostForScheduleDeleteView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    extra_context = {'segment': 'sched'}
    model = Post
    success_url = '/sched'
    template_name = 'crud/post_delete.html'
    success_message = 'Пост успешно Удалён!'


# BOTS #####################################################################

class BotListView(SuccessMessageMixin, LoginRequiredMixin, ListView):
    extra_context = {'segment': 'bs'}
    model = Bot
    template_name = 'home/bot_list.html'
    context_object_name = 'bots'


class BotUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Bot
    extra_context = {'segment': 'bot'}
    template_name = 'crud/bot_create.html'
    form_class = BotForm
    success_url = '/bot_list'
    success_message = 'Бот успешно обновлён!'


# POLLS #####################################################################


class PollListView(SuccessMessageMixin, LoginRequiredMixin, ListView):
    extra_context = {'segment': 'poll'}
    model = Poll
    paginate_by = 60
    template_name = 'home/poll_list.html'
    context_object_name = 'polls'
    success_message = 'Опрос успешно создан!'

    def get_queryset(self):
        qs = self.model.objects.filter(
            bot=UserSettings.objects.get(user=self.request.user).bot_selected).order_by('day', 'post_time')
        return qs


class PollCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Poll
    template_name = 'crud/poll_create.html'
    form_class = PollForm
    success_message = 'Опрос успешно добавлен!'

    def get_success_url(self):
        res = '/polls'
        if 'page' in self.request.GET:
            res += f"?page={self.request.GET['page']}"
        return res


class PollUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Poll
    template_name = 'crud/poll_create.html'
    form_class = PollForm
    success_message = 'Опрос успешно обновлён!'

    def get_success_url(self):
        res = '/polls'
        if 'page' in self.request.GET:
            res += f"?page={self.request.GET['page']}"
        return res


class PollDeleteView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = Poll
    success_url = '/polls'
    template_name = 'crud/poll_delete.html'
    success_message = 'Опрос успешно Удалён!'


@login_required(login_url="/login/")
def index(request):
    context = {
        'segment': 'index',
        'chats': Chat.objects.filter(bot=UserSettings.objects.get(user=request.user).bot_selected),
        'posts': Post.objects.filter(bot=UserSettings.objects.get(user=request.user).bot_selected, is_for_sched=False),
        'sched': Post.objects.filter(bot=UserSettings.objects.get(user=request.user).bot_selected, is_for_sched=True),
    }
    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def update_post_is_sent(request):
    context = {
        'segment': 'index',
        'chats': Chat.objects.all(),
        'posts': Post.objects.all(),
    }
    with transaction.atomic():
        model_qs = Post.objects.all()
        # model_bt = Bot.objects.all()
        for obj in model_qs:
            Post.objects.filter(bot=UserSettings.objects.get(user=request.user).bot_selected).update(is_sent=False)
            Chat.objects.filter(bot=UserSettings.objects.get(user=request.user).bot_selected).update(day=1)
            Bot.objects.filter(id=UserSettings.objects.get(user=request.user).bot_selected.id).update(is_started=False)
    # html_template = loader.get_template('home/post_list.html')
    # return HttpResponse(html_template.render(context, request))
    return redirect("/posts")


def ves_v_norme_redirect(request):
    return redirect('https://ves-v-norme.ru')


def change_bot_selected(request, id):
    UserSettings.objects.filter(user=request.user).update(bot_selected=Bot.objects.get(id=id))
    return redirect("/bot")
