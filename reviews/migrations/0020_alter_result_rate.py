# Generated by Django 4.1.10 on 2023-08-15 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0019_alter_competition_city'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='rate',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
