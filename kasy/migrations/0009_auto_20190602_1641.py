# Generated by Django 2.2 on 2019-06-02 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kasy', '0008_auto_20190601_2249'),
    ]

    operations = [
        migrations.AddField(
            model_name='kasa',
            name='nr_nadany',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='przeglad',
            name='data',
            field=models.DateField(default=0),
        ),
    ]