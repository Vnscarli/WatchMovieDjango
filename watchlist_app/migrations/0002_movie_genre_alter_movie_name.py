# Generated by Django 5.0.6 on 2024-06-25 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('watchlist_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='genre',
            field=models.CharField(default='Escolher'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='name',
            field=models.CharField(),
        ),
    ]
