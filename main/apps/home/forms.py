from django import forms

# from betterforms.multiform import MultiModelForm
# from emoji_picker.widgets import EmojiPickerTextInputAdmin, EmojiPickerTextareaAdmin, EmojiPickerTextarea, EmojiPickerTextInput
from .models import *
from ..middleware import current_user
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSettingsForm(forms.ModelForm):
    class Meta:
        model = UserSettings
        fields = ['primary_color', 'main_theme', 'tz']
        widgets = {
            'primary_color': forms.Select(attrs={'class': 'form-control text-info'}),
            'main_theme': forms.Select(attrs={'class': 'form-control text-info'}),
            'tz': forms.Select(attrs={'class': 'form-control text-info'}),
        }


class ChatForm(forms.ModelForm):
    class Meta:
        model = Chat
        fields = [
            'reference',
            'title',
        ]
        widgets = {
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
            # 'start_date': forms.DateTimeInput(attrs={'type': 'date'}),
            'day': forms.Select(attrs={'class': 'form-control text-info'}),
        }


class PostForm(forms.ModelForm):
    # text = forms.CharField(widget=EmojiPickerTextarea),

    class Meta:
        model = Post
        fields = [
            'day',
            'text',
            'media_file',
            'post_time',
            'is_sent',
            # 'post_type'
        ]
        widgets = {
            # 'post_type': forms.Select(attrs={'class': 'form-control text-info'}),
            'day': forms.Select(attrs={'class': 'form-control text-info'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': '...'}),
            'media_file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'post_time': forms.TimeInput(attrs={'class': 'form-control text-info', 'type': 'time'}),
        }


class PollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = [
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
