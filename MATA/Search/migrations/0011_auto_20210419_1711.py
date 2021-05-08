# Generated by Django 3.1.2 on 2021-04-19 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Search', '0010_auto_20210419_1706'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='item',
            name='last_name',
        ),
        migrations.AddField(
            model_name='item',
            name='description',
            field=models.TextField(default='', max_length=500),
        ),
        migrations.AlterField(
            model_name='item',
            name='reviewText',
            field=models.TextField(default='', max_length=5000),
        ),
    ]
