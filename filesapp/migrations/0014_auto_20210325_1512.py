# Generated by Django 3.1.7 on 2021-03-25 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filesapp', '0013_like'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='likes',
        ),
        migrations.AddField(
            model_name='image',
            name='post_likes_number',
            field=models.IntegerField(default=0),
        ),
    ]