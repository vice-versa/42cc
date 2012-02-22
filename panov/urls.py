# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from panov.views import PersonEditView


urlpatterns = patterns('panov.views',

    url(r'^$', 'index', name="index"),
    url(r'^request/list/$', 'request_list', name="request-list"),
    url(r'^person/edit/(?P<person_id>\d+)/$',
        PersonEditView.as_view(),
        name="person-edit"),
    url(r'^person/edit/$',
        PersonEditView.as_view(),
        name="person-edit-ajax"),
    url(r'accounts/login/$', 'login', name='login'),
    url(r'accounts/logout/$', 'logout', name='logout'),
    url(r'^history/$', 'history', name="history"),
    url(r'^person/edit/(?P<person_id>\d+)/upload/$',
        'upload',
        name="person-upload"),
                    )
