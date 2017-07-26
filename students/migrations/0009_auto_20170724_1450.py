# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-24 14:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0008_auto_20170724_1414'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exam',
            name='teacher_first_name',
        ),
        migrations.RemoveField(
            model_name='exam',
            name='teacher_last_name',
        ),
        migrations.RemoveField(
            model_name='exam',
            name='teacher_middle_name',
        ),
        migrations.AddField(
            model_name='exam',
            name='teacher_name',
            field=models.CharField(max_length=256, null=True, verbose_name='\u041f\u0406\u0411 \u0432\u0438\u043a\u043b\u0430\u0434\u0430\u0447\u0430'),
        ),
    ]
