#!/usr/bin/python
# -*- coding: utf-8 -*-

from rest_framework import serializers
from hc_practicas.serializers import EspecialidadNestedSerializer
from hc_practicas.models import Especialidad, Prestacion

class PrestacionNestedSerializer(serializers.ModelSerializer):
    """
    Serializa una especialidad, para ser incluida como objeto nested en otro objeto
    """
    id = serializers.IntegerField()
    name = serializers.ReadOnlyField()
    description = serializers.ReadOnlyField()
    status = serializers.ReadOnlyField()
    duration = serializers.ReadOnlyField()
    default = serializers.ReadOnlyField()
    notes = serializers.ReadOnlyField()

    url = serializers.HyperlinkedIdentityField(
        view_name='api:hc_practicas:Prestacion-detail',
        lookup_field='pk'
    )

    especialidad = EspecialidadNestedSerializer(
        many=False,
        read_only=True
    )

    def to_internal_value(self, data):
        prestaciones= Prestacion.objects.filter(pk=data['id'])
        if prestaciones.count() >0:
            return prestaciones[0]
        else:
            raise ValueError('Prestacion not found')


    class Meta:
        model = Prestacion
        fields = ('id', 'name', 'description', 'default', 'status', 'duration', 'default', 'notes', 'especialidad', 'url' )