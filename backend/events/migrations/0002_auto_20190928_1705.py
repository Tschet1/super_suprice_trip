# Generated by Django 2.2.5 on 2019-09-28 17:05

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='coordinates',
            field=django.contrib.gis.db.models.fields.PointField(null=True, srid=4326),
        ),
    ]
