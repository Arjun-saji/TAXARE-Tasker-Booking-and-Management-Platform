# Generated by Django 5.1.2 on 2024-10-28 10:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taskservices', '0003_alter_notification_recipient'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='booking',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='taskservices.booking'),
        ),
    ]
