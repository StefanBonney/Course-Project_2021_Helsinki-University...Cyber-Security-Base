# Generated by Django 4.0 on 2021-12-25 23:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CoinMiner', '0002_account_coin_coinamount_mineamount_delete_choice_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mineamount',
            old_name='votes',
            new_name='points',
        ),
    ]
