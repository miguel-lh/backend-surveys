# Generated by Django 5.0.9 on 2024-12-09 23:06

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0002_alter_historicalsurveys_type_alter_surveys_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='surveycomments',
            name='slug',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='uuid'),
        ),
    ]
