# Generated by Django 3.2.6 on 2021-08-27 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0020_alter_user_geo_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='geo_data',
            field=models.JSONField(default=dict),
        ),
    ]
