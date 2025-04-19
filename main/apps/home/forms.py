from django import forms
from .models import *
from django.contrib.auth import get_user_model, get_user

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
            'bot': forms.Select(attrs={'class': 'form-control text-info'}),
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
            'start_date': forms.DateTimeInput(format='%Y-%m-%d',
                                              attrs={'class': 'form-control text-info', 'type': 'date'}),
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

    # def __init__(self, *args, **kwargs):
    #     super(PostForm, self).__init__(*args, **kwargs)
    #     bot_selected = UserSettings.objects.get(user=User.objects.first()).bot_selected
    #     bot_set = Bot.objects.filter(id=bot_selected.id)
    #     self.fields['bot'].queryset = bot_set


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
            'sched_datetime': forms.DateTimeInput(format='%Y-%m-%dT%H:%M',
                                                  attrs={'class': 'form-control text-info', 'type': 'datetime-local'}),
            'is_for_sched': forms.CheckboxInput(attrs={'checked': ''}),
            'is_sent': forms.CheckboxInput(attrs={}),
        }

    def __init__(self, *args, **kwargs):
        super(PostForScheduleForm, self).__init__(*args, **kwargs)
        bot_selected = UserSettings.objects.get(user=User.objects.first()).bot_selected
        bot_set = Bot.objects.filter(id=bot_selected.id)
        self.fields['bot'].queryset = bot_set


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


class MessageToSendForm(forms.ModelForm):
    class Meta:
        model = MessageToSend
        fields = ['message_1', 'day_to_send_1_first', 'day_to_send_1_second', 'time_to_send_1',
                  'message_2', 'day_to_send_2_first', 'day_to_send_2_second', 'time_to_send_2']
        widgets = {
            'message_1': forms.Textarea(attrs={'class': 'form-text text-dark', 'placeholder': '...', }),
            'message_2': forms.Textarea(attrs={'class': 'form-text text-dark', 'placeholder': '...', }),
            'day_to_send_1_first': forms.Select(attrs={'class': 'form-control text-info'}),
            'day_to_send_1_second': forms.Select(attrs={'class': 'form-control text-info'}),
            'day_to_send_2_first': forms.Select(attrs={'class': 'form-control text-info'}),
            'day_to_send_2_second': forms.Select(attrs={'class': 'form-control text-info'}),
            'time_to_send_1': forms.TimeInput(attrs={'class': 'form-control text-info', 'type': 'time'}),
            'time_to_send_2': forms.TimeInput(attrs={'class': 'form-control text-info', 'type': 'time'}),
        }


class MessageToNotifyForm(forms.ModelForm):
    class Meta:
        model = MessageToNotify
        fields = ['bot', 'message', 'day_to_send_1', 'day_to_send_2', 'day_to_send_3', 'day_to_send_4', 'day_to_send_5',
                  'day_to_send_6', 'day_to_send_7', 'time_to_send']
        widgets = {
            'bot': forms.Select(attrs={'class': 'form-control text-info'}),
            'message': forms.Textarea(attrs={'class': 'form-text text-dark', 'placeholder': '...', }),
            'day_to_send_1': forms.Select(attrs={'class': 'form-control text-info'}),
            'day_to_send_2': forms.Select(attrs={'class': 'form-control text-info'}),
            'day_to_send_3': forms.Select(attrs={'class': 'form-control text-info'}),
            'day_to_send_4': forms.Select(attrs={'class': 'form-control text-info'}),
            'day_to_send_5': forms.Select(attrs={'class': 'form-control text-info'}),
            'day_to_send_6': forms.Select(attrs={'class': 'form-control text-info'}),
            'day_to_send_7': forms.Select(attrs={'class': 'form-control text-info'}),
            'time_to_send': forms.TimeInput(attrs={'class': 'form-control text-info', 'type': 'time'}),
        }
