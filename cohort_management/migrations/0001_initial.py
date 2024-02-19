# Generated by Django 5.0.2 on 2024-02-19 02:30

import django.db.models.deletion
import utils.snowflakes
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cohort',
            fields=[
                ('id', models.BigIntegerField(default=utils.snowflakes.Snowflake.generate_id, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('rules', models.TextField()),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='InternProfile',
            fields=[
                ('id', models.BigIntegerField(default=utils.snowflakes.Snowflake.generate_id, editable=False, primary_key=True, serialize=False)),
                ('role', models.CharField(choices=[('admin', 'Admin'), ('member', 'Member')], max_length=50)),
                ('certificate_id', models.BigIntegerField(null=True)),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField()),
                ('cohort', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cohort_management.cohort')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
