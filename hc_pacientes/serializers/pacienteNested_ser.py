#!/usr/bin/python
# -*- coding: utf-8 -*-

from rest_framework import serializers
from hc_practicas.models import Paciente
from hc_common.serializers import DocumentTypeNestedSerializer

class PacienteNestedSerializer(serializers.ModelSerializer):
    """
    Serializa un profesional, para ser incluida como objeto nested en otro objeto
    """

    id = serializers.IntegerField()
    firstName=serializers.ReadOnlyField()
    otherNames=serializers.ReadOnlyField()
    fatherSurname=serializers.ReadOnlyField()
    motherSurname=serializers.ReadOnlyField()
    birthDate=serializers.ReadOnlyField()
    documentType= DocumentTypeNestedSerializer(
        many=False,
        read_only=True
    )
    documentNumber=serializers.ReadOnlyField()
    email=serializers.ReadOnlyField()
    primaryPhoneNumber=serializers.ReadOnlyField()
    primaryPhoneContact=serializers.ReadOnlyField()
    primaryPhoneMessage=serializers.ReadOnlyField()

    url = serializers.HyperlinkedIdentityField(
        view_name='hc_pacientes:Paciente-detail',
        lookup_field='pk'
    )

    def to_internal_value(self, data):
        pacientes= Paciente.objects.filter(pk=data['id'])
        if paciente.count()>0:
            return paciente[0]
        else:
            raise ValueError('Paciente not found')


    class Meta:
        model = Paciente
        fields = ('id', 'firstName', 'otherNames', 'fatherSurname', 'motherSurname', 'birthDate', 'documentType', 'documentNumber', 'email','primaryPhoneNumber', 'primaryPhoneContact', 'primaryPhoneMessage', 'url')