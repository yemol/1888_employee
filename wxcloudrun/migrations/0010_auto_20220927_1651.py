# Generated by Django 3.2.8 on 2022-09-27 16:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wxcloudrun', '0009_auto_20220927_1650'),
    ]

    operations = [
        migrations.AlterField(
            model_name='counters',
            name='createdAt',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 27, 16, 51, 10, 751417)),
        ),
        migrations.AlterField(
            model_name='counters',
            name='updatedAt',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 27, 16, 51, 10, 751443)),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='createdAt',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 27, 16, 51, 10, 752607)),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='updatedAt',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 27, 16, 51, 10, 752624)),
        ),
        migrations.AlterField(
            model_name='users',
            name='createdAt',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 27, 16, 51, 10, 751869)),
        ),
        migrations.AlterField(
            model_name='users',
            name='updatedAt',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 27, 16, 51, 10, 751884)),
        ),
    ]
