# Generated by Django 3.2.7 on 2022-08-23 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Dress_Fit', '0006_alter_video_activity_video_url'),
    ]

    operations = [
        migrations.RenameField(
            model_name='video_activity',
            old_name='PerformanceRange',
            new_name='End_Range',
        ),
        migrations.AddField(
            model_name='video_activity',
            name='Start_Range',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
