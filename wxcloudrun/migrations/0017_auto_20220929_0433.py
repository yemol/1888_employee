# Generated by Django 3.2.8 on 2022-09-29 04:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wxcloudrun', '0016_auto_20220928_0508'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='createdAt',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 29, 4, 33, 10, 707832)),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='updatedAt',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 29, 4, 33, 10, 707847)),
        ),
        migrations.AlterField(
            model_name='users',
            name='createdAt',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 29, 4, 33, 10, 706988)),
        ),
        migrations.AlterField(
            model_name='users',
            name='nickName',
            field=models.CharField(default='', max_length=256),
        ),
        migrations.AlterField(
            model_name='users',
            name='updatedAt',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 29, 4, 33, 10, 707017)),
        ),
    ]