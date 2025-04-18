# Generated by Django 4.2.4 on 2023-10-13 20:22

import apps.home.validators
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0015_auto_20230511_1125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='day',
            field=models.IntegerField(blank=True, choices=[(1, 'День 1'), (2, 'День 2'), (3, 'День 3'), (4, 'День 4'), (5, 'День 5'), (6, 'День 6'), (7, 'День 7'), (8, 'День 8'), (9, 'День 9'), (10, 'День 10'), (11, 'День 11'), (12, 'День 12'), (13, 'День 13'), (14, 'День 14'), (15, 'День 15'), (16, 'День 16'), (17, 'День 17'), (18, 'День 18'), (19, 'День 19'), (20, 'День 20'), (21, 'День 21'), (22, 'День 22'), (23, 'День 23'), (24, 'День 24'), (25, 'День 25'), (26, 'День 26'), (27, 'День 27'), (28, 'День 28'), (29, 'День 29'), (30, 'День 30'), (31, 'День 31')], default=1, max_length=100, null=True, verbose_name='День, с которого начнутся публикации'),
        ),
        migrations.AlterField(
            model_name='post',
            name='media_file',
            field=models.FileField(blank=True, null=True, upload_to='', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'mp3', 'mp4', 'mpeg', 'avi', 'mkv']), apps.home.validators.validate_non_ascii], verbose_name='Медиа файл'),
        ),
    ]
