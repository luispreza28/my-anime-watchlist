# Generated by Django 4.2.2 on 2023-09-14 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('watchlist', '0003_rename_episode_length_anime_members_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='anime',
            name='description',
            field=models.TextField(blank=True, max_length=600, null=True),
        ),
    ]
