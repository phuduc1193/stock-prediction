# Generated by Django 2.2 on 2019-04-01 23:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StockSector',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('slug', models.CharField(max_length=50)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('symbol', models.CharField(max_length=10, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('website', models.CharField(max_length=50)),
                ('ceo', models.CharField(max_length=100)),
                ('sector', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='data_storage.StockSector')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='StockPrice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('high', models.DecimalField(decimal_places=4, max_digits=15)),
                ('low', models.DecimalField(decimal_places=4, max_digits=15)),
                ('open', models.DecimalField(decimal_places=4, max_digits=15)),
                ('close', models.DecimalField(decimal_places=4, max_digits=15)),
                ('volume', models.IntegerField()),
                ('timestamp', models.DateTimeField()),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data_storage.Company')),
            ],
            options={
                'ordering': ['company', '-timestamp'],
                'unique_together': {('company', 'timestamp')},
            },
        ),
    ]
