#!/usr/bin/python
# -*- coding: utf-8 -*-

from rest_framework import generics
from rest_framework.permissions import AllowAny
from hc_practicas.serializers import PeriodNestSerializer
from hc_practicas.models import Period
from hc_core.views.paginateListCreateAPIView import PaginateListCreateAPIView


class PeriodList(PaginateListCreateAPIView):
    serializer_class = PeriodNestSerializer
    queryset = Period.objects.all()


class PeriodDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PeriodNestSerializer
    queryset = Period.objects.all()
