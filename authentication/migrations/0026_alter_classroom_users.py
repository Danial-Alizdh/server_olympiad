# Generated by Django 4.1.10 on 2023-09-27 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0025_alter_classroom_users'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classroom',
            name='users',
            field=models.ManyToManyField(to='authentication.userprofile', verbose_name='افراد شرکت\u200cکننده'),
        ),
    ]
