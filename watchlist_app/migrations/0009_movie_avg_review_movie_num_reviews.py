# Generated by Django 5.0.6 on 2024-07-25 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('watchlist_app', '0008_review_editor'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='avg_review',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='movie',
            name='num_reviews',
            field=models.IntegerField(default=0),
        ),
    ]
