# Generated by Django 3.1.3 on 2021-04-17 12:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0009_auto_20210416_2130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='status',
            field=models.CharField(default='P', max_length=1),
        ),
        migrations.AlterField(
            model_name='routine',
            name='end_time',
            field=models.TimeField(default=datetime.time(12, 37, 4, 911028)),
        ),
        migrations.AlterField(
            model_name='routine',
            name='start_time',
            field=models.TimeField(default=datetime.time(12, 37, 4, 911028)),
        ),
    ]