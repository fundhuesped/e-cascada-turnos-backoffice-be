#!/usr/bin/python
# -*- coding: utf-8 -*-

from rest_framework import serializers
from hc_notificaciones.models import NotificationSMS
import requests
from django.conf import settings
import sys  
# I don't know what this is used for, but it generates an error. The commit says something about 
# reload(sys)
# sys.setdefaultencoding('utf8')

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
            turno=validated_data.get('turno'),
            paciente=validated_data.get('paciente')
        )
        notificacion.save()
        self.send_notification(notificacion)
        return notificacion


    def send_notification(self, notificacion):
        if settings.USE_NOTIFICATION_HUB:
            data = self.data.copy()
            data['reference_id'] = notificacion.id
            response = requests.post(settings.NOTIFICATION_HUB_SMS_URL+"/api/notificaciones/smsNotification/", data=data, headers={"Authorization":"Token "+settings.NOTIFICATION_HUB_TOKEN})
        else:
            url = settings.BASE_SMS_URL
            url = url + "enviar_sms.asp?api=1"
            url = url + "&usuario=" + settings.SMS_SERVICE_USER
            url = url + "&clave=" + settings.SMS_SERVICE_PASSWORD
            url = url + "&tos=" + notificacion.destination
            url = url + "&texto=" + notificacion.message
            url = url + "&instance=CMH" 
            if self.context.get('reference_id') is not None:
                url = url + "&idinterno=" + str(self.context.get('reference_id'))
            else:
                url = url + "&idinterno=" + str(notificacion.id)
            url = url + "&respuestanumerica=1"

            response = requests.get(url)
        print(response.text)
        splitted_response = response.text.split(";")

        if splitted_response[0] == "0":
            notificacion.state = NotificationSMS.STATE_SENT
        else:
            notificacion.state = NotificationSMS.STATE_ERROR
        notificacion.save()

        return response

    class Meta:
        model = NotificationSMS
        fields = ('id', 'destination', 'message', 'state', 'turno', 'paciente')
