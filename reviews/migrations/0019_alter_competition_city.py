# Generated by Django 4.1.10 on 2023-08-10 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0018_alter_result_city'),
    ]

    operations = [
        migrations.AlterField(
            model_name='competition',
            name='city',
            field=models.CharField(default='', max_length=2000),
        ),
    ]
