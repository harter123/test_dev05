# Generated by Django 3.2.11 on 2022-05-15 03:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_api', '0013_auto_20220423_1200'),
    ]

    operations = [
        migrations.AddField(
            model_name='htestplan',
            name='not_start_num',
            field=models.IntegerField(default=0, verbose_name='未开始个数'),
        ),
    ]
