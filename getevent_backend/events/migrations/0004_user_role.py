# Generated by Django 4.2.16 on 2024-12-17 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_organizer_event_organizer'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('user', 'User'), ('organizer', 'Organizer')], default='user', max_length=10),
        ),
    ]