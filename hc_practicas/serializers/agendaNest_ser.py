#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import transaction
from rest_framework import serializers
from hc_practicas.models import Agenda, Period, DayOfWeek, Profesional, Prestacion, Turno
from hc_practicas.serializers import PeriodNestSerializer, ProfesionalNestedSerializer, PrestacionNestedSerializer
import datetime as dt
import calendar
from django.db.models import Max
from django.utils.translation import gettext as _

class AgendaNestSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    periods = PeriodNestSerializer(
        many=True
    )

    profesional = ProfesionalNestedSerializer(
        many=False
    )

    prestacion = PrestacionNestedSerializer(
        many=False
    )

    def getFromDate(self, profesional, prestacion):
        """
        Obtiene la fecha desde la cual se debe crear una agenda para un profesional y una prestación dada
        :param profesional:
        :param prestacion:
        :return:
        """
        fromDate = dt.datetime.now().date()
        #Filtrado de agenda por profesional y prestación
        queryset = Agenda.objects.filter(profesional = profesional, prestacion=prestacion)

        if queryset.count()>0:
            maxDate = queryset.aggregate(Max('validTo'))['rating__max'] ##TODO:probar bien
            day = maxDate.day
            month = maxDate.month
            year = maxDate.year
            if(day==calendar.monthrange(year, month)): ##Si es el ultimo dia del mes
                fromDate = dt.date(year=year if month <12 else year+1, month= month+1 if month < 12 else 1, day=1)
            else:
                fromDate = dt.date(year=year, month=month, day=day+1)
        return fromDate

    def getToDate(self, fromDate):
        """
        Devuelve el máximo día del mes en el cual una agenda debe ser creada.
        :param fromDate:
        :return:
        """
        month = fromDate.month
        year = fromDate.year
        maxday = calendar.monthrange(year, month)[1]
        return dt.date(year=year, month=month, day=maxday)

    def validate(self, attrs):
        profesional = attrs['profesional']
        prestacion = attrs['prestacion']

        if not prestacion in profesional.prestaciones.all():
            raise serializers.ValidationError({'Prestacion': _('La prestacion no coincide con el profesional')})
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        profesional = validated_data.pop('profesional')
        prestacion = validated_data.pop('prestacion')
        validFrom = validated_data.get('validFrom')
        validFrom = validFrom if validFrom is not None else self.getFromDate(profesional, prestacion)
        validTo = validated_data.get('validTo')
        validTo = validTo if validTo is not None else self.getToDate(validFrom)

        instance = Agenda.objects.create(
            status=validated_data.get('status'),
            start=validated_data.get('start'),          #Hora inicio de turnos
            end=validated_data.get('end'),              #Hora fin de turnos
            validFrom=validFrom,                        #Fecha desde la cual se debe crear la agenda
            validTo=validTo,                            #Fecha hasta la cual se debe crear la agenda
            profesional=profesional,                 #Profesional para el cual se desea crear una agenda
            prestacion=prestacion                    #Prestación para la cual se desea crear una agenda
        )
        periods = validated_data.pop('periods')
        return self.load_agenda(periods, instance, profesional, prestacion)

    @transaction.atomic
    def update(self, instance, validated_data):
        profesional = validated_data.pop('profesional')
        prestacion = validated_data.pop('prestacion')
        instance.status = validated_data.get('status', instance.status)
        instance.start = validated_data.get('start', instance.start)
        instance.end = validated_data.get('end', instance.end)
        instance.validFrom = validated_data.get('validFrom', instance.validFrom)
        instance.validTo = validated_data.get('validTo', instance.validTo)
        instance.profesional = profesional
        instance.prestacion = prestacion

        for period in instance.periods.all():
            for dayOfWeek in period.daysOfWeek.all():
                dayOfWeek.delete()
            period.delete()

        instance.periods.clear()
        periods = validated_data.pop('periods')

        return self.load_agenda(periods, instance, profesional, prestacion)

    def load_agenda(self, periods, agenda_instance, profesional, prestacion):
        for period in periods:
            period_instance = Period.objects.create(
                start=period.get('start'),
                end=period.get('end'),
                selected=period.get('selected')
            )

            days_of_week = period.pop('daysOfWeek')
            for dayOfWeek in days_of_week:
                """
                day_instance = DayOfWeek.objects.create(
                    index=dayOfWeek.get('index'),
                    name=dayOfWeek.get('name'),
                    selected=dayOfWeek.get('selected')
                )
                day_instance.save()
                """
                period_instance.daysOfWeek.add(dayOfWeek)
                self.insert_period_days(agenda_instance, period_instance, dayOfWeek, profesional, prestacion)

            period_instance.save()
            agenda_instance.periods.add(period_instance)

        return agenda_instance

    def insert_period_days(self, agenda, period, day_of_week, profesional, prestacion):
        start_date = agenda.validFrom
        end_date = agenda.validTo

        total_days = (end_date - start_date).days + 1

        for day_number in range(total_days):
            current_date = (start_date + dt.timedelta(days=day_number))
            if current_date.weekday() == day_of_week.index:
                if day_of_week.selected is True:
                    turno_instance = Turno.objects.create(
                        day=current_date,
                        start=period.start,
                        end=period.end,
                        profesional=profesional,
                        prestacion=prestacion
                    )
                    turno_instance.save()

    class Meta:
        model = Agenda
        fields = ('id', 'status', 'start', 'end', 'validFrom', 'validTo', 'periods', 'profesional', 'prestacion')
