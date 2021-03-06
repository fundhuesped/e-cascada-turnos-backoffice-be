#!/usr/bin/python
# -*- coding: utf-8 -*-

from rest_framework import generics, filters
from rest_framework.permissions import DjangoModelPermissions
from hc_practicas.serializers import TurnoNestSerializer
from hc_practicas.models import Turno
from hc_core.views import PaginateListCreateAPIView

class TurnoList(PaginateListCreateAPIView):
    """
    Vista para listar los elementos y crear uno nuevo
    """
    serializer_class = TurnoNestSerializer
    queryset = Turno.objects.all()
    permission_classes = (DjangoModelPermissions,)
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('turnoSlot__day')
    ordering = ('-turnoSlot__day')

    def get_queryset(self):
        queryset = Turno.objects.all()
        informed = self.request.query_params.get('informed')

        if informed is not None:
            value = self.str2bool(informed)
            queryset = queryset.filter(informed=value)

        paciente = self.request.query_params.get('paciente')
        if paciente is not None:
            queryset = queryset.filter(paciente=paciente)

        agenda = self.request.query_params.get('agenda')
        if agenda is not None:
            queryset = queryset.filter(turnoSlot__agenda=agenda)

        cancelation_reason = self.request.query_params.get('cancelation_reason')
        if cancelation_reason is not None:
            queryset = queryset.filter(cancelation_reason__in=cancelation_reason.split(','))

        day__range_start = self.request.query_params.get('day__range_start')
        day__range_end = self.request.query_params.get('day__range_end')
        if day__range_start is not None and day__range_end is not None:
            queryset = queryset.filter(turnoSlot__day__range=(day__range_start, day__range_end))

        status = self.request.query_params.get('status')
        if status is not None:
            queryset = queryset.filter(status=status)

        state = self.request.query_params.get('state')
        if state is not None:
            queryset = queryset.filter(state=state)

        profesional = self.request.query_params.get('profesional')
        if profesional is not None:
            queryset = queryset.filter(turnoSlot__profesional=profesional)

        prestacion = self.request.query_params.get('prestacion')
        if prestacion is not None:
            queryset = queryset.filter(turnoSlot__prestacion=prestacion)

        turno_slot = self.request.query_params.get('turnoSlot')
        if turno_slot is not None:
            queryset = queryset.filter(turnoSlot=turno_slot)

        return queryset

    def str2bool(self, v):
        return v.lower() in ("yes", "true", "t", "1")

class TurnoDetails(generics.RetrieveUpdateDestroyAPIView):
    """
    Vista para solicitar un recurso y modificarlo
    """
    serializer_class = TurnoNestSerializer
    queryset = Turno.objects.all()
    permission_classes = (DjangoModelPermissions,)
