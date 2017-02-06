# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-02-06 01:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hc_notificaciones', '0004_basenotificationresponse_responseaction'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailNotificationResponse',
            fields=[
                ('basenotificationresponse_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='hc_notificaciones.BaseNotificationResponse')),
                ('notification', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notification', to='hc_notificaciones.NotificationEmail')),
            ],
            options={
                'abstract': False,
            },
            bases=('hc_notificaciones.basenotificationresponse',),
        ),
    ]
