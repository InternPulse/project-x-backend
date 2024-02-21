# Generated by Django 5.0.2 on 2024-02-20 15:14

import utils.snowflakes
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0006_alter_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.BigIntegerField(default=utils.snowflakes.Snowflake.generate_id, editable=False, primary_key=True, serialize=False),
        ),
    ]
