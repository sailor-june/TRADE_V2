# Generated by Django 4.1.5 on 2023-03-06 00:11

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("main_app", "0004_tradeoffer"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="profile",
            name="inventory",
        ),
    ]
