#!/usr/bin/python
# -*- coding: utf-8 -*-

from rest_framework import generics
from rest_framework.permissions import AllowAny
from procedures.serializers import PeriodSerializer
from procedures.models import Period

class PeriodList(generics.ListCreateAPIView):
    """
    Vista para listar Period existentes, o crear un nuevo Period
    """
    serializer_class = PeriodSerializer
    queryset = Period.objects.all()
    permission_classes = (AllowAny,)
    paginate_by = 20

class PeriodDetails(generics.RetrieveUpdateDestroyAPIView):
    """
    Vista para ver del detalle, modificar, o eliminar un Period
    """
    serializer_class = PeriodSerializer
    queryset = Period.objects.all()
    permission_classes = (AllowAny,)
