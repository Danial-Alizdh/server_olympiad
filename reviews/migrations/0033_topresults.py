# Generated by Django 4.1.10 on 2023-08-31 13:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0032_championship'),
    ]

    operations = [
        migrations.CreateModel(
            name='TopResults',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('gold', models.EmailField(max_length=254, verbose_name='طلا')),
                ('silver', models.TextField(verbose_name='نقره')),
                ('bronze', models.TextField(verbose_name='برنز')),
                ('game_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reviews.game', verbose_name='نام بازی')),
            ],
            options={
                'verbose_name': 'نتایج برتر',
                'verbose_name_plural': 'نتایج برتر (در صفحه اول)',
            },
        ),
    ]
