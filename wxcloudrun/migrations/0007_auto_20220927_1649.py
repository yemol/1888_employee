# Generated by Django 3.2.8 on 2022-09-27 16:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wxcloudrun', '0006_auto_20220927_1641'),
    ]

    operations = [
        migrations.AlterField(
            model_name='counters',
            name='createdAt',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 27, 16, 49, 3, 534239)),
        ),
        migrations.AlterField(
            model_name='counters',
            name='updatedAt',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 27, 16, 49, 3, 534270)),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='createdAt',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 27, 16, 49, 3, 535654)),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='updatedAt',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 27, 16, 49, 3, 535670)),
        ),
        migrations.AlterField(
            model_name='users',
            name='createdAt',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 27, 16, 49, 3, 534818)),
        ),
        migrations.AlterField(
            model_name='users',
            name='updatedAt',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 27, 16, 49, 3, 534840)),
        ),
    ]