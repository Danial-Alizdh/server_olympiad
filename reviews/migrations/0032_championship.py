# Generated by Django 4.1.10 on 2023-08-20 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0031_news_link'),
    ]

    operations = [
        migrations.CreateModel(
            name='Championship',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100, verbose_name='عنوان')),
                ('images', models.ManyToManyField(related_name='championships', to='reviews.image')),
            ],
            options={
                'verbose_name': 'پایگاه قهرمانی',
                'verbose_name_plural': 'پایگاه قهرمانی',
            },
        ),
    ]
