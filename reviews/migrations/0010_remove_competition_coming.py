# Generated by Django 4.1.10 on 2023-08-09 19:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0009_remove_competition_cities_competition_city_game_sex_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='competition',
            name='coming',
        ),
    ]
