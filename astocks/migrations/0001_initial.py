# Generated by Django 4.0.2 on 2022-02-03 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StockList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ts_code', models.CharField(max_length=50, unique=True)),
                ('symbol', models.CharField(max_length=10, unique=True)),
                ('name', models.CharField(max_length=50, unique=True)),
                ('area', models.CharField(max_length=50)),
                ('industry', models.CharField(max_length=50)),
                ('list_date', models.CharField(max_length=50)),
            ],
        ),
    ]
