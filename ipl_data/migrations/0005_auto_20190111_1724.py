# Generated by Django 2.1.5 on 2019-01-11 17:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ipl_data', '0004_auto_20190111_1723'),
    ]

    operations = [
        migrations.RenameField(
            model_name='deliveries',
            old_name='match',
            new_name='match_id',
        ),
    ]
