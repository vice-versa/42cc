# -*- coding: utf-8 -*-
from django.conf import settings as django_settings


def settings(request):

    context = {
               'settings': django_settings
               }

    return context
