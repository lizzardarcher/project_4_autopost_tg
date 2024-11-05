from django import forms
from .models import *
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSettingsForm(forms.ModelForm):
    class Meta:
        model = UserSettings
        fields = ['primary_color', 'main_theme', 'tz', 'bot_selected']
        widgets = {
            'bot_selected': forms.Select(attrs={'class': 'form-control text-dark'}),
            'primary_color': forms.Select(attrs={'class': 'form-control text-info'}),
            'main_theme': forms.Select(attrs={'class': 'form-control text-info'}),
            'tz': forms.Select(attrs={'class': 'form-control text-info'}),
        }


class ChatForm(forms.ModelForm):
    class Meta:
        model = Chat
        fields = [
            'bot',
            'reference',
            'title',
        ]
        widgets = {
            'bot':forms.Select(attrs={'class': 'form-control text-info'}),
            'reference': forms.TextInput(attrs={'class': 'form-control text-info'}),
            'title': forms.TextInput(attrs={'class': 'form-control text-info'}),
        }


class BotForm(forms.ModelForm):
    class Meta:
        model = Bot
        fields = ['ref', 'token', 'title', 'start_date', 'is_started', 'day']
        widgets = {
            'ref': forms.TextInput(attrs={'class': 'form-control text-info'}),
            'token': forms.TextInput(attrs={'class': 'form-control text-info'}),
            'title': forms.TextInput(attrs={'class': 'form-control text-info'}),
            'day': forms.Select(attrs={'class': 'form-control text-info'}),
        }


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'bot',
            'day',
            'text',
            'media_file',
            'post_time',
            'is_sent',
        ]
        widgets = {
            'bot': forms.Select(attrs={'class': 'form-control text-info'}),
            'day': forms.Select(attrs={'class': 'form-control text-info'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': '...'}),
            'media_file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'post_time': forms.TimeInput(attrs={'class': 'form-control text-info', 'type': 'time'}),
        }


class PostForScheduleForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = [
            'bot',
            'text',
            'media_file',
            'sched_datetime',
            'is_for_sched',
            'is_sent',
        ]
        widgets = {
            'bot': forms.Select(attrs={'class': 'form-control text-info'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': '...'}),
            'media_file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'sched_datetime': forms.DateTimeInput(attrs={'class': 'form-control text-info', 'type': 'datetime-local'}),
            'is_for_sched': forms.CheckboxInput(attrs={'checked': ''}),
            'is_sent': forms.CheckboxInput(attrs={}),
        }


class PollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = [
            'bot',
            'day',
            'post_time',
            'question',
            'is_sent',
            'option_1',
            'option_2',
            'option_3',
            'option_4',
            'option_5',
            'option_6',
            'option_7',
            'option_8',
            'option_9',
            'option_10'
        ]
        widgets = {
            'bot': forms.Select(attrs={'class': 'form-control text-info'}),
            'day': forms.Select(attrs={'class': 'form-control text-info'}),
            'post_time': forms.TimeInput(attrs={'class': 'form-control text-info', 'type': 'time'}),
            'question': forms.Textarea(attrs={'class': 'form-control', 'placeholder': '...'}),
            'option_1': forms.Textarea(attrs={'class': 'form-control', 'placeholder': '...'}),
            'option_2': forms.Textarea(attrs={'class': 'form-control', 'placeholder': '...'}),
            'option_3': forms.Textarea(attrs={'class': 'form-control', 'placeholder': '...'}),
            'option_4': forms.Textarea(attrs={'class': 'form-control', 'placeholder': '...'}),
            'option_5': forms.Textarea(attrs={'class': 'form-control', 'placeholder': '...'}),
            'option_6': forms.Textarea(attrs={'class': 'form-control', 'placeholder': '...'}),
            'option_7': forms.Textarea(attrs={'class': 'form-control', 'placeholder': '...'}),
            'option_8': forms.Textarea(attrs={'class': 'form-control', 'placeholder': '...'}),
            'option_9': forms.Textarea(attrs={'class': 'form-control', 'placeholder': '...'}),
            'option_10': forms.Textarea(attrs={'class': 'form-control', 'placeholder': '...'}),
        }


class PostToUserForm(forms.ModelForm):
    fields = '__all__'

