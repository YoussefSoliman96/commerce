# Generated by Django 4.2.5 on 2023-10-01 18:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_comment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='comment',
            new_name='listingComment',
        ),
    ]