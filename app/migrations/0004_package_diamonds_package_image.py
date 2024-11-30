# Generated by Django 5.1.3 on 2024-11-28 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_game_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='package',
            name='diamonds',
            field=models.PositiveIntegerField(default=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='package',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='package_images'),
        ),
    ]