# Generated by Django 5.0.3 on 2024-03-11 14:06

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='YoutubeFilterTracker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('category', models.PositiveBigIntegerField(blank=True, null=True)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('channels', models.TextField()),
                ('video_tags', models.TextField(blank=True)),
                ('logs', models.JSONField(null=True, verbose_name='JSON data set')),
                ('share_count', models.PositiveIntegerField(default=0)),
                ('user_rating', models.PositiveIntegerField(blank=True, choices=[(1, '1 Star'), (2, '2 Stars'), (3, '3 Stars'), (4, '4 Stars'), (5, '5 Stars')], null=True)),
                ('privacy_level', models.CharField(choices=[('Public', 'Public'), ('Private', 'Private')], default='Private', max_length=7)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Youtube Filter Tracker',
                'ordering': ['-id'],
            },
        ),
    ]