# Generated by Django 2.2.1 on 2019-05-29 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kasy', '0003_auto_20190525_0917'),
    ]

    operations = [
        migrations.AddField(
            model_name='przeglad',
            name='info',
            field=models.TextField(blank=True, null=True),
        ),
    ]
