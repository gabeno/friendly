# Generated by Django 3.2.6 on 2021-08-26 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_post_likes_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='author_id',
            field=models.IntegerField(default=99),
        ),
    ]
