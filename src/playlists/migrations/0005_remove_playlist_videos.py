# Generated by Django 4.1.2 on 2022-11-02 16:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("playlists", "0004_playlistitem"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="playlist",
            name="videos",
        ),
    ]