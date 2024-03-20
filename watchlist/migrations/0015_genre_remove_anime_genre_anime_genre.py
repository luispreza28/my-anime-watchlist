# Generated by Django 4.2.2 on 2024-01-09 22:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('watchlist', '0014_rename_anime_type_anime_genre'),
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='anime',
            name='genre',
        ),
        migrations.AddField(
            model_name='anime',
            name='genre',
            field=models.ManyToManyField(to='watchlist.genre'),
        ),
    ]
