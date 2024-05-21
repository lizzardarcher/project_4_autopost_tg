# -*- encoding: utf-8 -*-
import os
import requests
import urllib.request
from urllib.request import urlopen
from tempfile import NamedTemporaryFile

from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.core.validators import FileExtensionValidator
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

from . import validators

tz_choice = [
    ('-12 International Date Line West', '-12 UTC International Date Line West'),
    ('-11 Coordinated Universal Time-11', '-11 UTC Coordinated Universal Time-11'),
    ('-10 Hawaii', '-10 UTC Hawaii'),
    ('-09 Alaska', '-09 UTC Alaska'),
    ('-08 Pacific Time (US & Canada)', '-08 UTC Pacific Time (US & Canada)'),
    ('-07 Mountain Time (US & Canada)', '-07 UTC Mountain Time (US & Canada)'),
    ('-06 Central Time (US & Canada)', '-06 UTC Central Time (US & Canada)'),
    ('-05 Eastern Time (US & Canada)', '-05 UTC Eastern Time (US & Canada)'),
    ('-04 Georgetown, La Paz, Manaus, San Juan', '-04  UTC Georgetown, La Paz, Manaus, San Juan'),
    ('-03 Buenos Aires', '-03 UTC Buenos Aires'),
    ('-02 Coordinated Universal Time-02', '-02 UTC Coordinated Universal Time-02'),
    ('-01 Cape Verde Is.', '-01 UTC Cape Verde Is.'),
    ('+00 Dublin, Edinburgh, Lisbon, London', '+00 UTC Dublin, Edinburgh, Lisbon, London'),
    ('+01 Brussels, Copenhagen, Madrid, Paris', '+01 UTC Brussels, Copenhagen, Madrid, Paris'),
    ('+02 E. Europe', '+02 UTC E. Europe'),
    ('+03 Baghdad', '+03 UTC Baghdad'),
    ('+04 Moscow', '+04 UTC Moscow'),
    ('+04 SPB', '+04 UTC SPB'),
    ('+05 Ashgabat, Tashkent', '+05 UTC Ashgabat, Tashkent'),
    ('+06 Yekaterinburg', '+06 UTC Yekaterinburg'),
    ('+07 Novosibirsk', '+07 UTC Novosibirsk'),
    ('+08 Krasnoyarsk', '+08 UTC Krasnoyarsk'),
    ('+09 Irkutsk', '+09 UTC Irkutsk'),
    ('+10 Canberra, Melbourne, Sydney', '+10 UTC Canberra, Melbourne, Sydney'),
    ('+11 Vladivostok', '+11 UTC Vladivostok'),
    ('+12 Magadan', '+12 UTC Magadan'),
    ('+13 Samoa', '+13 UTC Samoa'),
]
day_choice = [
    (1, 'День 1'), (2, 'День 2'), (3, 'День 3'), (4, 'День 4'), (5, 'День 5'), (6, 'День 6'),
    (7, 'День 7'), (8, 'День 8'), (9, 'День 9'), (10, 'День 10'), (11, 'День 11'), (12, 'День 12'),
    (13, 'День 13'), (14, 'День 14'), (15, 'День 15'), (16, 'День 16'), (17, 'День 17'), (18, 'День 18'),
    (19, 'День 19'), (20, 'День 20'), (21, 'День 21'), (22, 'День 22'), (23, 'День 23'), (24, 'День 24'),
    (25, 'День 25'), (26, 'День 26'), (27, 'День 27'), (28, 'День 28'), (29, 'День 29'), (30, 'День 30'),
    (31, 'День 31'),
]
allowed_extensions = ['jpg',
                      'jpeg',
                      'mp3',
                      'mp4',
                      'mpeg',
                      'avi',
                      'mkv',
                      ]

POST_TYPE = [
    ('Пост', 'Пост'),
    ('Опрос', 'Опрос'),
]


class UserSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # start_time = models.IntegerField(default=1, null=True, blank=True, verbose_name='Start Parser In (time)')
    primary_color = models.CharField(max_length=100,
                                     choices=[('primary', 'Розовый'), ('blue', 'Синий'), ('orange', 'Оранжевый'),
                                              ('red', 'Красный'), ('green', 'Зеленый')],
                                     default='Розовый', blank=True, verbose_name='Основной цвет приложения')
    main_theme = models.CharField(max_length=100, choices=[('white-content', 'Светлый'), ('', 'Тёмный')],
                                  default='Тёмный',
                                  blank=True, verbose_name='Тема')
    tz = models.CharField(max_length=100, blank=True, default='+06 Yekaterinburg', choices=tz_choice, verbose_name='Time Zone')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Settings'

class Bot(models.Model):

    ref = models.CharField(max_length=100, verbose_name='Ссылка на бота', validators=[validators.validate_bot_ref_https])
    token = models.CharField(max_length=300, verbose_name='Бот Токен')
    title = models.CharField(max_length=300, null=True, blank=True, verbose_name='Назавание бота')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    start_date = models.DateField(null=True, blank=True, verbose_name='Начало работы Бота')
    is_started = models.BooleanField(null=True, blank=True, default=False, verbose_name='Старт бота')
    day = models.IntegerField(max_length=100, null=False, blank=False, default=1, choices=day_choice,  verbose_name='День по порядку публикации')
    id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['id']
        verbose_name = "Бот"
        verbose_name_plural = "Боты"

class Post(models.Model):
    day = models.IntegerField(max_length=100, null=False, blank=False, choices=day_choice,  verbose_name='День по порядку публикации')
    # user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Пользователь')
    text = models.TextField(max_length=1000, null=True, blank=True, verbose_name='Текст')
    # post_type = models.CharField(max_length=50, default='Пост', blank=False, choices=POST_TYPE, verbose_name='Тип сообщения')
    is_sent = models.BooleanField(null=True, blank=True, default=False, verbose_name='Отправлено')
    media_file = models.FileField(validators=[
        FileExtensionValidator(allowed_extensions=allowed_extensions),
        validators.validate_non_ascii], null=True, blank=True, verbose_name='Медиа файл')
    post_time = models.TimeField(null=True, blank=True, verbose_name='Время публикации')
    id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return str(self.id)

    class Meta:
        # ordering = ['id']
        verbose_name = "Пост"
        verbose_name_plural = "Посты"

class Poll(models.Model):
    day = models.IntegerField(max_length=100, null=False, blank=False, choices=day_choice,  verbose_name='День по порядку публикации')
    is_sent = models.BooleanField(null=True, blank=True, default=False, verbose_name='Отправлено')
    post_time = models.TimeField(null=True, blank=True, verbose_name='Время публикации')

    question = models.TextField(max_length=1000, null=False, blank=False, verbose_name='Вопрос')
    option_1 = models.TextField(max_length=500, null=False, blank=False, verbose_name='Вариант 1')
    option_2 = models.TextField(max_length=500, null=True, blank=True, verbose_name='Вариант 2')
    option_3 = models.TextField(max_length=500, null=True, blank=True, verbose_name='Вариант 3')
    option_4 = models.TextField(max_length=500, null=True, blank=True, verbose_name='Вариант 4')
    option_5 = models.TextField(max_length=500, null=True, blank=True, verbose_name='Вариант 5')
    option_6 = models.TextField(max_length=500, null=True, blank=True, verbose_name='Вариант 6')
    option_7 = models.TextField(max_length=500, null=True, blank=True, verbose_name='Вариант 7')
    option_8 = models.TextField(max_length=500, null=True, blank=True, verbose_name='Вариант 8')
    option_9 = models.TextField(max_length=500, null=True, blank=True, verbose_name='Вариант 9')
    option_10 = models.TextField(max_length=500, null=True, blank=True, verbose_name='Вариант 10')
    is_anonymous = models.BooleanField(null=True, blank=True, default=True, verbose_name='Анонимный опрос')
    id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return str(self.id)

    class Meta:
        # ordering = ['id']
        verbose_name = "Опрос"
        verbose_name_plural = "Опросы"

class Chat(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Пользователь')
    reference = models.CharField(max_length=200, null=True, unique=True, validators=[validators.validate_contains_https], verbose_name='Ссылка на чат')
    title = models.CharField(max_length=300, null=True, blank=True, verbose_name='Название чата')
    # image = models.CharField(max_length=1000, null=True, blank=True, verbose_name='Ссылка на изображение канала')
    image = models.ImageField(max_length=5000, null=True, blank=True, verbose_name='Изображение чата')
    image_url = models.URLField(max_length=5000, blank=True, null=True)
    error = models.CharField(max_length=1000, null=True, blank=True, verbose_name='Ошибки')
    day = models.IntegerField(max_length=100, null=True, blank=True, default=1, choices=day_choice,  verbose_name='День, с которого начнутся публикации')
    chat_id = models.BigIntegerField(default=0, null=True, blank=True, verbose_name='ID чата')
    id = models.AutoField(primary_key=True, editable=False)

    def save(self, *args, **kwargs):
        if self.image_url and not self.image and 'data:image' not in self.image_url:
            # Сохраняем аватарку из чата
            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(urlopen(self.image_url).read())
            img_temp.flush()
            self.image.save(f"image_{self.pk}.jpg", File(img_temp))
            self.save()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Чат'
        verbose_name_plural = 'Чаты'
        ordering = ['id']

    def __str__(self):
        return self.title

class UserToMail(models.Model):
    id = models.IntegerField(verbose_name='User ID', primary_key=True)

    class Meta:
        verbose_name = 'Пользователь для рассылки'
        verbose_name_plural = 'Пользователи для рассылки'

    def __str__(self):
        return str(self.id)