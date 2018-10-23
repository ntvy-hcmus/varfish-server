# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-10-15 13:16
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [("users", "0001_initial")]

    operations = [
        migrations.AlterModelOptions(name="user", options={}),
        migrations.AddField(
            model_name="user",
            name="sodar_uuid",
            field=models.UUIDField(default=uuid.uuid4, help_text="User SODAR UUID", unique=True),
        ),
    ]
