# Generated by Django 3.1.7 on 2021-05-08 20:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Index',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(default='', max_length=128)),
                ('des_tf', models.IntegerField(default=0)),
                ('title_tf', models.IntegerField(default=0)),
                ('review_tf', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('description', models.TextField()),
                ('asin', models.CharField(max_length=10)),
                ('image', models.TextField(default='', max_length=500)),
                ('title_length', models.IntegerField(default=0)),
                ('desc_length', models.IntegerField(default=0)),
                ('review_length', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('length', models.IntegerField(default=0)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Search.item')),
            ],
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('des_df', models.IntegerField()),
                ('title_df', models.IntegerField()),
                ('review_df', models.IntegerField()),
                ('index', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Search.index')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Search.item')),
            ],
        ),
        migrations.AddField(
            model_name='index',
            name='items',
            field=models.ManyToManyField(through='Search.Membership', to='Search.Item'),
        ),
    ]
