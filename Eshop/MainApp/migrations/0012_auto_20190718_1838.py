# Generated by Django 2.2.2 on 2019-07-18 13:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MainApp', '0011_auto_20190708_1251'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='brand',
        ),
        migrations.RemoveField(
            model_name='product',
            name='cat',
        ),
        migrations.RemoveField(
            model_name='product',
            name='color',
        ),
    ]