# Generated by Django 4.1.10 on 2023-09-15 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0007_remove_userprofile_id_alter_userprofile_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='username',
            field=models.CharField(default='noName', max_length=50),
        ),
    ]
