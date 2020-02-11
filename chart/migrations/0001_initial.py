# Generated by Django 2.2.5 on 2019-11-09 11:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('stock_id', models.CharField(help_text='the Stock ID of a Company', max_length=6, primary_key=True, serialize=False)),
                ('company_name', models.CharField(help_text='the Name of a Company', max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='StockSeries',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateField(blank=True)),
                ('high', models.FloatField(blank=True, null=True)),
                ('low', models.FloatField(blank=True, null=True)),
                ('open', models.FloatField(blank=True, null=True)),
                ('close', models.FloatField(blank=True, null=True)),
                ('ofWhich', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='chart.Company', unique=None)),
            ],
            options={
                'verbose_name': 'StockSeries',
                'ordering': ['ofWhich'],
            },
        ),
    ]