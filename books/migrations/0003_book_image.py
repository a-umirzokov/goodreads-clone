# Generated by Django 4.2.10 on 2024-02-13 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='image',
            field=models.ImageField(blank=True, default='default-book-cover.png', null=True, upload_to='media-files'),
        ),
    ]