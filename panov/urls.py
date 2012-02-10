# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *


urlpatterns = patterns('panov.views',

    url(r'^$', 'index', name="index"),
    url(r'^request/list/$', 'request_list', name="request-list"),
    url(r'^history/$', 'history', name="history"),
                    )
