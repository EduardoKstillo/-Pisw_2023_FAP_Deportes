# Generated by Django 4.2.3 on 2024-01-10 01:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('championship', '0002_alter_game_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='state',
            field=models.BooleanField(default=False),
        ),
    ]
