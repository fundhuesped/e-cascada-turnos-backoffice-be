#!/usr/bin/python
# -*- coding: utf-8 -*-

from rest_framework import serializers
from hc_common.models import District
from hc_common.serializers import ProvinceNestSerializer


class DistrictNestSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    name = serializers.ReadOnlyField()
    description = serializers.ReadOnlyField()
    status = serializers.ReadOnlyField()

    province = ProvinceNestSerializer(
        many=False
    )

    def create(self, validated_data):
        province = validated_data.pop('province')
        district = District.objects.create(
            name=validated_data.get('name'),
            description=validated_data.get('description'),
            status=validated_data.get('status'),
            province=province
        )
        return district

    def update(self, instance, validated_data):
        province = validated_data.pop('province')
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.status = validated_data.get('status', instance.status)
        instance.province = province
        instance.save()

        return instance

    class Meta:
        model = District
        fields = ('id', 'status', 'name', 'description', 'province')
