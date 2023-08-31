# Generated by Django 4.1.10 on 2023-08-18 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0029_delete_cultural'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cultural',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100, verbose_name='عنوان')),
                ('images', models.ManyToManyField(related_name='culturals', to='reviews.image')),
            ],
            options={
                'verbose_name': 'فرهنگی',
                'verbose_name_plural': 'فرهنگی\u200cها',
            },
        ),
    ]