# Generated by Django 4.1.10 on 2023-09-27 10:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0029_alter_joinedclass_id_alter_userprofile_phone_number'),
    ]

    operations = [
        migrations.RenameField(
            model_name='joinedclass',
            old_name='board_email',
            new_name='classroom',
        ),
        migrations.RenameField(
            model_name='joinedclass',
            old_name='user_email',
            new_name='user',
        ),
    ]
