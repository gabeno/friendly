# Generated by Django 3.2.6 on 2021-08-26 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_user_created_when'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(default='example@mail.com', max_length=50, unique=True),
        ),
    ]