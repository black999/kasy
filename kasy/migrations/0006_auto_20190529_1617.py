# Generated by Django 2.2.1 on 2019-05-29 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kasy', '0005_auto_20190529_1615'),
    ]

    operations = [
        migrations.AlterField(
            model_name='przeglad',
            name='info',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
    ]
