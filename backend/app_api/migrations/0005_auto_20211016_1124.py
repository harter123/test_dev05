# Generated by Django 3.2.5 on 2021-10-16 03:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_api', '0004_testresult_testtask'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='testtask',
            name='cases',
        ),
        migrations.CreateModel(
            name='TaskCaseRelevance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('case_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_api.testcase')),
                ('task_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_api.testtask')),
            ],
        ),
    ]