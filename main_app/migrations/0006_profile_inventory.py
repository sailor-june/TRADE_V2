# Generated by Django 4.1.5 on 2023-03-06 15:08

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main_app", "0005_remove_profile_inventory"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="inventory",
            field=models.ManyToManyField(to="main_app.item"),
        ),
    ]
