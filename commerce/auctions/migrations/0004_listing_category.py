# Generated by Django 3.1.5 on 2021-03-05 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_auto_20210304_1822'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='category',
            field=models.CharField(choices=[('CL', 'Clothing'), ('EL', 'Electronics'), ('BK', 'Books'), ('GR', 'Groceries'), ('FT', 'Footwear'), ('PL', 'Plants'), ('ST', 'Stationary'), ('OT', 'Other')], default='OT', max_length=2),
        ),
    ]