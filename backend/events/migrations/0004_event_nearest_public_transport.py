# Generated by Django 2.2.5 on 2019-09-28 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_auto_20190928_1743'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='nearest_public_transport',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
