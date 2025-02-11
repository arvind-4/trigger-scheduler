# Generated by Django 5.1.6 on 2025-02-11 10:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("eventlogs", "0002_alter_eventlog_trigger"),
        ("triggers", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="eventlog",
            name="trigger",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="triggers.trigger",
            ),
        ),
    ]
