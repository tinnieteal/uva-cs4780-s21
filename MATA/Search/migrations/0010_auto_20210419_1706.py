# Generated by Django 3.1.2 on 2021-04-19 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Search', '0009_auto_20210419_1705'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='reviewText',
            field=models.CharField(default='', max_length=5000),
        ),
    ]