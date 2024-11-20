# Generated by Django 4.2.16 on 2024-10-11 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('location', models.CharField(max_length=255)),
                ('date', models.DateTimeField()),
                ('is_private', models.BooleanField(default=False)),
                ('password', models.CharField(blank=True, max_length=5, null=True)),
            ],
        ),
    ]
