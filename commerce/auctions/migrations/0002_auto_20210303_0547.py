# Generated by Django 3.1.5 on 2021-03-03 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='status',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='listing',
            name='winnner',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
