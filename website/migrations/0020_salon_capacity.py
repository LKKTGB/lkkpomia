# Generated by Django 2.0.2 on 2018-06-11 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0019_video_contest_winner_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='salon',
            name='capacity',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]
