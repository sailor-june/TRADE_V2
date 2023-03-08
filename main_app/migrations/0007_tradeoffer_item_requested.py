# Generated by Django 4.1.5 on 2023-03-08 15:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("main_app", "0006_profile_inventory"),
    ]

    operations = [
        migrations.AddField(
            model_name="tradeoffer",
            name="item_requested",
            field=models.ForeignKey(
                default=9,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="received_trade_offers",
                to="main_app.item",
            ),
            preserve_default=False,
        ),
    ]