# Generated by Django 3.1.2 on 2021-04-19 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Search', '0008_item_reviewtext'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='reviewText',
            field=models.TextField(default='', max_length=5000),
        ),
    ]
