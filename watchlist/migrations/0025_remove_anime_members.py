# Generated by Django 4.2.2 on 2024-03-20 18:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('watchlist', '0024_alter_anime_genre'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='anime',
            name='members',
        ),
    ]
