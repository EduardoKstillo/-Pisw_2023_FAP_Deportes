# Generated by Django 4.2.3 on 2023-10-11 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('championship', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='image',
            field=models.ImageField(default=0, upload_to='pics'),
            preserve_default=False,
        ),
    ]
