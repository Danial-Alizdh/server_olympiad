# Generated by Django 4.1.10 on 2023-09-16 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0009_alter_userprofile_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pics'),
        ),
    ]