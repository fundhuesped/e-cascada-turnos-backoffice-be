#!/usr/bin/python
# -*- coding: utf-8 -*-

from rest_framework import generics
from rest_framework.permissions import AllowAny
from hc_common.serializers import CivilStatusTypeSerializer
from hc_common.models import CivilStatusType


class CivilStatusTypeList(generics.ListCreateAPIView):
    serializer_class = CivilStatusTypeSerializer
    queryset = CivilStatusType.objects.all()
    permission_classes = (AllowAny,)
    paginate_by = 20

    def get_queryset(self):
        queryset = CivilStatusType.objects.all()
        name = self.request.query_params.get('name')
        status = self.request.query_params.get('status')
        if name is not None:
            queryset = queryset.filter(name__startswith=name)
        if status is not None:
            queryset = queryset.filter(status=status)
        return queryset


class CivilStatusTypeDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CivilStatusTypeSerializer
    queryset = CivilStatusType.objects.all()
    permission_classes = (AllowAny,)