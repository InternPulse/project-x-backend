# Generated by Django 5.0.2 on 2024-02-20 15:14

import utils.snowflakes
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0005_alter_defermentticket_id_alter_notification_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='defermentticket',
            name='id',
            field=models.BigIntegerField(default=utils.snowflakes.Snowflake.generate_id, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='notification',
            name='id',
            field=models.BigIntegerField(default=utils.snowflakes.Snowflake.generate_id, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='paymentticket',
            name='id',
            field=models.BigIntegerField(default=utils.snowflakes.Snowflake.generate_id, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='talentrequestticket',
            name='id',
            field=models.BigIntegerField(default=utils.snowflakes.Snowflake.generate_id, editable=False, primary_key=True, serialize=False),
        ),
    ]