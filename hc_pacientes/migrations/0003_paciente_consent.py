# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-06-26 22:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hc_pacientes', '0002_initial_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='paciente',
            name='consent',
            field=models.CharField(choices=[(b'Yes', b'Si'), (b'No', b'No'), (b'Not asked', b'No preguntado')], default=b'Not asked', max_length=14),
        ),
    ]
