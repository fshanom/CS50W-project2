# Generated by Django 3.1.1 on 2020-09-25 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_auto_20200925_1516'),
    ]

    operations = [
        migrations.AddField(
            model_name='bids',
            name='date',
            field=models.DateTimeField(auto_now_add=True, default=None),
            preserve_default=False,
        ),
    ]