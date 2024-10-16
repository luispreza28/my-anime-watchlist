# Generated by Django 4.2.2 on 2023-09-14 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('watchlist', '0002_anime_type_alter_anime_episode_length'),
    ]

    operations = [
        migrations.RenameField(
            model_name='anime',
            old_name='episode_length',
            new_name='members',
        ),
        migrations.RemoveField(
            model_name='anime',
            name='description',
        ),
        migrations.RemoveField(
            model_name='anime',
            name='genre',
        ),
        migrations.RemoveField(
            model_name='anime',
            name='image',
        ),
        migrations.RemoveField(
            model_name='anime',
            name='release_date',
        ),
        migrations.RemoveField(
            model_name='anime',
            name='type',
        ),
        migrations.AddField(
            model_name='anime',
            name='aired_on',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='anime',
            name='anime_type',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='anime',
            name='myanimelist_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='anime',
            name='myanimelist_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='anime',
            name='picture_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='anime',
            name='rank',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='anime',
            name='score',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True),
        ),
        migrations.AlterField(
            model_name='useranimelist',
            name='status',
            field=models.CharField(choices=[('currently_watching', 'Currently Watching'), ('completed', 'Completed'), ('on_hold', 'On Hold'), ('dropped', 'Dropped'), ('plan_to_watch', 'Plan to Watch')], default='plan_to_watch', max_length=50),
        ),
    ]
