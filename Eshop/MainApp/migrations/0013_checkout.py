# Generated by Django 2.2.2 on 2019-07-18 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MainApp', '0012_auto_20190718_1838'),
    ]

    operations = [
        migrations.CreateModel(
            name='Checkout',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chname', models.CharField(max_length=30)),
                ('mobile', models.IntegerField()),
                ('email', models.EmailField(max_length=50)),
                ('state', models.CharField(max_length=30)),
                ('city', models.CharField(max_length=30)),
                ('address', models.CharField(max_length=50)),
                ('pin', models.CharField(max_length=10)),
            ],
        ),
    ]