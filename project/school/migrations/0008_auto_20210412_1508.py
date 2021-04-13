# Generated by Django 3.1.3 on 2021-04-12 09:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0007_auto_20210408_2145'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='routine',
            name='time',
        ),
        migrations.AddField(
            model_name='routine',
            name='end_time',
            field=models.TimeField(default=datetime.time(15, 8, 43, 720699)),
        ),
        migrations.AddField(
            model_name='routine',
            name='start_time',
            field=models.TimeField(default=datetime.time(15, 8, 43, 720699)),
        ),
    ]
