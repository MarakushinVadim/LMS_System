# Generated by Django 4.2 on 2024-07-02 19:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("materials", "0003_subscription"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="subscription",
            name="name",
        ),
    ]
