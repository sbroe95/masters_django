# Generated by Django 4.0.4 on 2022-05-01 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('masters_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('player_name', models.TextField()),
                ('odds_points', models.IntegerField()),
            ],
        ),
    ]