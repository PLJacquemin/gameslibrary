# Generated by Django 4.1.5 on 2023-04-04 09:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('GamesLibrary', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='video_game',
            old_name='plateform',
            new_name='platform',
        ),
    ]
