# Generated by Django 4.1.10 on 2023-09-17 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0012_userprofile_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='role',
            field=models.CharField(choices=[('کاربر عادی', 'کاربر عادی'), ('مربی', 'مربی'), ('سالن\u200cدار', 'سالن\u200cدار')], default='کاربر عادی', max_length=10, verbose_name='نقش کاربر'),
        ),
    ]
