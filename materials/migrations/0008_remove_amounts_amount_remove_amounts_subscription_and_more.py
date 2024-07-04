# Generated by Django 4.2 on 2024-07-04 19:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "materials",
            "0007_remove_subscription_link_remove_subscription_product_and_more",
        ),
    ]

    operations = [
        migrations.RemoveField(
            model_name="amounts",
            name="amount",
        ),
        migrations.RemoveField(
            model_name="amounts",
            name="subscription",
        ),
        migrations.RemoveField(
            model_name="subscription",
            name="amount",
        ),
        migrations.AddField(
            model_name="amounts",
            name="course",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="materials.course",
                verbose_name="Курс",
            ),
        ),
    ]