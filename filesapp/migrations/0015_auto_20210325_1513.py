# Generated by Django 3.1.7 on 2021-03-25 09:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('filesapp', '0014_auto_20210325_1512'),
    ]

    operations = [
        migrations.RenameField(
            model_name='image',
            old_name='post_likes_number',
            new_name='likes',
        ),
    ]
