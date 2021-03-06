#!/usr/bin/python
# -*- coding: utf-8 -*-

import reversion
from django.db import models
from hc_common.models import ActiveModel
import reversion

@reversion.register()
class Especialidad(ActiveModel):

    name = models.CharField(max_length=70, null=False)
    description = models.CharField(max_length=150, null=True, blank=True)
    status = models.CharField(max_length=8, choices=ActiveModel.STATUS_CHOICES, default=ActiveModel.STATUS_ACTIVE)
    default = models.BooleanField(default=False)

    class Meta:
        ordering = ['-default','name']