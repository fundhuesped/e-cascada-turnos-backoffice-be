#!/usr/bin/python
# -*- coding: utf-8 -*-

from rest_framework import serializers
from hc_notificaciones.models import NotificationSMS
import requests
from django.conf import settings


class NotificationSMSSerializer(serializers.ModelSerializer):
    """
    Serializa una notificacion por SMS
    """
    id = serializers.ReadOnlyField()

    def create(self, validated_data):
        notificacion = NotificationSMS.objects.create(
            destination=validated_data.get('destination'),
            message=validated_data.get('message'),
            state=NotificationSMS.STATE_INITIAL,
            notificationtype=NotificationSMS.NOTIFICATION_TYPE_SMS,
        )
        self.send_notification(notificacion)
        return notificacion


    def send_notification(self, notificacion):
        url = settings.BASE_SMS_URL
        url = url + "enviar_sms.asp?api=1"
        url = url + "&usuario=" + settings.SMS_SERVICE_USER
        url = url + "&clave=" + settings.SMS_SERVICE_PASSWORD
        url = url + "&tos=" + notificacion.destination
        url = url + "&texto=" + notificacion.message
        response = requests.get(url)
        return response

    class Meta:
        model = NotificationSMS
        fields = ('id', 'destination', 'message', 'state')
