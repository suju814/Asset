# Generated by Django 3.1.6 on 2021-03-19 06:47

from django.db import migrations, models
import filesapp.models


class Migration(migrations.Migration):

    dependencies = [
        ('filesapp', '0005_auto_20210319_1214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(blank=True, height_field='image_height', null=True, upload_to=filesapp.models.generate_post_name, width_field='image_width'),
        ),
    ]
