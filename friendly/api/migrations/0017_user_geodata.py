# Generated by Django 3.2.6 on 2021-08-27 05:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_alter_user_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='geodata',
            field=models.JSONField(default='{}'),
        ),
    ]
