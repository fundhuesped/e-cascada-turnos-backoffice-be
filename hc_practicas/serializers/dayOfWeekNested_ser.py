#!/usr/bin/python
# -*- coding: utf-8 -*-

from rest_framework import serializers
from hc_practicas.models import DayOfWeek

class DayOfWeekNestedSerializer(serializers.ModelSerializer):
    """
    Serializa un DayOfWeek, para ser incluida como objeto nested en otro objeto
    """

    id = serializers.IntegerField()
    start = serializers.ReadOnlyField()
    index = serializers.ReadOnlyField()
    name = serializers.ReadOnlyField()
    selected = serializers.ReadOnlyField()


    url = serializers.HyperlinkedIdentityField(
        view_name='hc_practicas:DayOfWeek-detail',
        lookup_field='pk'
    )

    def to_internal_value(self, data):
        try:
            days= DayOfWeek.objects.filter(pk=data['id'])
            if days.count()>0:
                return days[0]
            else:
                return None # ValueError('DaysOfWeek not found')
        except:
            return None


    class Meta:
        model = DayOfWeek
        fields = ('id', 'start', 'index', 'name', 'selected', 'url')