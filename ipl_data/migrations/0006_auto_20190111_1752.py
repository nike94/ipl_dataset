# Generated by Django 2.1.5 on 2019-01-11 17:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ipl_data', '0005_auto_20190111_1724'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deliveries',
            name='match_id',
        ),
        migrations.AddField(
            model_name='deliveries',
            name='match',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='ipl_data.Matches'),
        ),
    ]