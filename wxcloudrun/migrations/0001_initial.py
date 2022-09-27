# Generated by Django 3.2.8 on 2022-09-27 02:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Counters',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(default=0, max_length=11)),
                ('createdAt', models.DateTimeField(default=datetime.datetime(2022, 9, 27, 2, 56, 57, 429986))),
                ('updatedAt', models.DateTimeField(default=datetime.datetime(2022, 9, 27, 2, 56, 57, 430029))),
            ],
            options={
                'db_table': 'Counters',
            },
        ),
    ]
