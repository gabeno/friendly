# Generated by Django 3.2.6 on 2021-08-27 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0023_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='title',
        ),
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.CharField(max_length=300),
        ),
    ]