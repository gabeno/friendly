# Generated by Django 3.2.6 on 2021-08-31 18:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20210831_1827'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='likes_count',
            new_name='likes',
        ),
    ]