# Generated by Django 4.2.4 on 2023-08-09 11:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0005_alter_news_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='news',
            old_name='img',
            new_name='image',
        ),
    ]
