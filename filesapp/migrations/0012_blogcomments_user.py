# Generated by Django 3.1.7 on 2021-03-25 06:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('filesapp', '0011_auto_20210325_1131'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogcomments',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='auth.user', verbose_name='User'),
            preserve_default=False,
        ),
    ]
