# Generated by Django 4.1.10 on 2023-08-10 13:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0016_result_attention_result_description_result_file_link_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='result',
            old_name='description',
            new_name='city',
        ),
    ]
