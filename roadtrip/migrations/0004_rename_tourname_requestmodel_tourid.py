# Generated by Django 3.2 on 2021-05-09 09:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('roadtrip', '0003_waypointsmodel_placeid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='requestmodel',
            old_name='tourname',
            new_name='tourid',
        ),
    ]
