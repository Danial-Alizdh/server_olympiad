# Generated by Django 4.1.10 on 2023-08-31 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0034_alter_topresults_bronze_alter_topresults_gold_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='topresults',
            name='game_id',
        ),
        migrations.AddField(
            model_name='topresults',
            name='city',
            field=models.CharField(default='', max_length=1000, verbose_name='استان'),
        ),
    ]
