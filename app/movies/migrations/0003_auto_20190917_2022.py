# Generated by Django 2.2.5 on 2019-09-17 20:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_auto_20190917_1823'),
    ]

    operations = [
        migrations.RenameField(
            model_name='film',
            old_name='average_rating',
            new_name='cache_average_rating',
        ),
        migrations.RenameField(
            model_name='film',
            old_name='num_votes',
            new_name='cache_num_votes',
        ),
    ]
