# Generated by Django 4.2.5 on 2023-10-02 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_bid_alter_auctionlisting_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.CharField(default=2000, max_length=600),
            preserve_default=False,
        ),
    ]
