#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime as dt
from django.db import transaction
from django.utils.translation import gettext as _
from rest_framework import serializers
from hc_practicas.models import Profesional, Prestacion, Turno
from hc_pacientes.models import Paciente
from hc_pacientes.serializers import PacienteNestedSerializer
from hc_practicas.serializers import ProfesionalNestedSerializer, PrestacionNestedSerializer


class TurnoNestSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    paciente = PacienteNestedSerializer(
        many=False
    )

    profesional = ProfesionalNestedSerializer(
        many=False
    )

    prestacion = PrestacionNestedSerializer(
        many=False
    )

    def create(self, validated_data):
        profesional = validated_data.pop('profesional')
        prestacion = validated_data.pop('prestacion')
        paciente = validated_data.pop('paciente')
        instance = Turno.objects.create(
            day=validated_data.get('day'),
            start=validated_data.get('start'),
            end=validated_data.get('end'),
            taken=validated_data.get('taken'),
            profesional=profesional,
            prestacion=prestacion,
            paciente=paciente
        )

        return instance

    @transaction.atomic
    def update(self, instance, validated_data):
        profesional = validated_data.pop('profesional')
        prestacion = validated_data.pop('prestacion')
        paciente = validated_data.pop('paciente')
        taken = validated_data.get('taken')

        #Nuevo estado de turnos para el mismo período de tiempo, para el profesional en cuestión.
        #Si taken = true (se confirma un nuevo turno para el profesional) y instance.taken = false (no estaba tomado el turno), se deben inhabilitar los turnos (status_turnos_asociados = 'Inactive')
        #Si taken = false (se libera un turno para el profesional) y instance.taken = true (estaba tomado el turno), se deben habilitar los turnos asociados (status_turnos_asociados='Active')
        #En otro caso, solo modificar datos del turno.


        if taken and not instance.taken:
#
#           Tomo el turno y no modifico sus demas datos
#
            return self.take_turn(instance, paciente)
        elif not taken and instance.taken:
#
#           Suelto el turno y no modifico sus demas datos
#
            return self.release_turn(instance)
        else:
#
#           Modifico datos del turno menos el paciente o su estado de taken
#
            instance.day = validated_data.get('day', instance.day)
            instance.start = validated_data.get('start', instance.start)
            instance.end = validated_data.get('end', instance.end)
            instance.profesional = profesional
            instance.prestacion = prestacion
            instance.save()


            return instance

    @transaction.atomic
    def take_turn(self, instance, paciente):
        """
        Toma un turno para un paciente y marca los demas turnos que colisionan
        """

        if instance.day < dt.date.today():
            raise serializers.ValidationError({'error': _('No se pueden tomar turnos ya pasados')})
        instance.paciente = paciente
        instance.status = Turno.STATUS_ACTIVE
        instance.taken = True
        instance.save()

        self.cambiar_status_turnos_asociados(instance.day,
                                             instance.start,
                                             instance.end,
                                             instance.profesional,
                                             Turno.STATUS_INACTIVE,
                                             instance.id)
        return instance

    @transaction.atomic
    def release_turn(self, instance):
        """
        Libera un turno y marca los demas turnos que colisionan
        """
        if instance.day < dt.date.today():
            raise serializers.ValidationError({'error': _('No se pueden liberar turnos ya pasados')})

        instance.paciente = None
        instance.status = Turno.STATUS_ACTIVE
        instance.taken = False
        instance.save()

        self.cambiar_status_turnos_asociados(instance.day,
                                             instance.start,
                                             instance.end,
                                             instance.profesional,
                                             Turno.STATUS_ACTIVE,
                                             instance.id)
        return instance

    def cambiar_status_turnos_asociados(self, day, start, end, profesional, status, original_turno_id):
        turnos = Turno.objects.filter(day=day,profesional=profesional).exclude(pk=original_turno_id)
        for turno in turnos:
            if (turno.end == end) or (turno.start == start) or (turno.start < start and turno.end > end) or (turno.start >= start and turno.start < end) or (turno.end > start and turno.end <= end):
                turno.status = status if status is not None else turno.status
                turno.save()
    class Meta:
        model = Turno
        fields = ('id', 'day', 'start', 'end', 'taken', 'paciente', 'profesional', 'prestacion', 'status')
