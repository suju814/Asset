# Generated by Django 3.1.7 on 2021-03-29 09:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('filesapp', '0024_auto_20210329_1406'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='download',
            options={},
        ),
        migrations.RemoveField(
            model_name='download',
            name='date',
        ),
        migrations.AddField(
            model_name='download',
            name='total_downloads',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='download',
            name='po',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Download_name', to='filesapp.image'),
        ),
    ]
