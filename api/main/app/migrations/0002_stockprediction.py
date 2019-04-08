# Generated by Django 2.2 on 2019-04-08 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StockPrediction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.CharField(max_length=10, unique=True)),
                ('upper', models.DecimalField(decimal_places=4, max_digits=15)),
                ('lower', models.DecimalField(decimal_places=4, max_digits=15)),
                ('estimate', models.DecimalField(decimal_places=4, max_digits=15)),
                ('date', models.DateTimeField()),
            ],
            options={
                'ordering': ['-date'],
                'unique_together': {('symbol', 'date')},
            },
        ),
    ]