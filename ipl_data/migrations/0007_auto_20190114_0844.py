# Generated by Django 2.1.5 on 2019-01-14 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ipl_data', '0006_auto_20190111_1752'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deliveries',
            name='batsman_runs',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='deliveries',
            name='extra_runs',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='deliveries',
            name='legbye_runs',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='deliveries',
            name='noball_runs',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='deliveries',
            name='penalty_runs',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='deliveries',
            name='total_runs',
            field=models.IntegerField(default=0),
        ),
    ]
