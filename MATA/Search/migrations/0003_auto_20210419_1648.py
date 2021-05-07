# Generated by Django 3.1.2 on 2021-04-19 20:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Search', '0002_auto_20210419_1628'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='asin',
        ),
        migrations.RemoveField(
            model_name='item',
            name='description',
        ),
        migrations.RemoveField(
            model_name='item',
            name='image',
        ),
        migrations.RemoveField(
            model_name='item',
            name='title',
        ),
        migrations.AddField(
            model_name='item',
            name='first_name',
            field=models.CharField(default=1, max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='item',
            name='last_name',
            field=models.CharField(default=1, max_length=30),
            preserve_default=False,
        ),
    ]
