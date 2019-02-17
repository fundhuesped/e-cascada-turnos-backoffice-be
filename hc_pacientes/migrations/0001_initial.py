# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2018-01-23 19:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('hc_common', '0002_initial_data'),
    ]

    operations = [
        migrations.CreateModel(
            name='Paciente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prospect', models.BooleanField(default=False)),
                ('consent', models.CharField(choices=[(b'Yes', b'Si'), (b'No', b'No'), (b'Not asked', b'No preguntado')], default=b'Not asked', max_length=14)),
                ('updated_on', models.DateField(auto_now=True)),
                ('firstName', models.CharField(default=b'No informado', max_length=80)),
                ('otherNames', models.CharField(blank=True, max_length=80, null=True)),
                ('fatherSurname', models.CharField(default=b'No informado', max_length=80)),
                ('motherSurname', models.CharField(blank=True, max_length=40, null=True)),
                ('alias', models.CharField(blank=True, max_length=80, null=True)),
                ('hceNumber', models.CharField(blank=True, max_length=20, null=True)),
                ('birthDate', models.DateField(blank=True, null=True)),
                ('documentNumber', models.CharField(blank=True, max_length=15, null=True)),
                ('email', models.CharField(blank=True, max_length=100, null=True)),
                ('status', models.CharField(choices=[(b'Active', b'Activo'), (b'Inactive', b'Inactivo')], default=b'Active', max_length=8)),
                ('street', models.CharField(blank=True, max_length=150, null=True)),
                ('postal', models.CharField(blank=True, max_length=20, null=True)),
                ('occupation', models.CharField(blank=True, max_length=150, null=True)),
                ('socialServiceNumber', models.CharField(blank=True, max_length=30, null=True)),
                ('bornPlace', models.CharField(blank=True, max_length=50, null=True)),
                ('firstVisit', models.DateField(blank=True, null=True)),
                ('notes', models.CharField(blank=True, max_length=200, null=True)),
                ('primaryPhoneNumber', models.CharField(blank=True, max_length=20, null=True)),
                ('primaryPhoneContact', models.CharField(blank=True, max_length=40, null=True)),
                ('primaryPhoneMessage', models.NullBooleanField(default=False)),
                ('secondPhoneNumber', models.CharField(blank=True, max_length=20, null=True)),
                ('secondPhoneContact', models.CharField(blank=True, max_length=40, null=True)),
                ('secondPhoneMessage', models.NullBooleanField(default=False)),
                ('thirdPhoneNumber', models.CharField(blank=True, max_length=20, null=True)),
                ('thirdPhoneContact', models.CharField(blank=True, max_length=40, null=True)),
                ('thirdPhoneMessage', models.NullBooleanField(default=False)),
                ('civilStatus', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='hc_common.CivilStatusType')),
                ('documentType', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hc_common.DocumentType')),
                ('education', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='hc_common.EducationType')),
                ('genderAtBirth', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pacienteGenderBirth', to='hc_common.SexType')),
                ('genderOfChoice', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pacienteGenderChoice', to='hc_common.SexType')),
                ('location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pacienteLocation', to='hc_common.Location')),
                ('socialService', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='hc_common.SocialService')),
            ],
            options={
                'ordering': ['fatherSurname'],
            },
        ),
    ]
