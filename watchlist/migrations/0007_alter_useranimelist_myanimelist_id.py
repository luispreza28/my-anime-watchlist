# Generated by Django 4.2.2 on 2023-09-22 21:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('watchlist', '0006_useranimelist_myanimelist_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useranimelist',
            name='myanimelist_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='watchlist.anime'),
        ),
    ]
