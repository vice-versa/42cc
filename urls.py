# -*- coding: utf-8 -*-

import os

from django.conf import settings
from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


"""
urlpatterns = patterns('42cc.views',

)
"""
urlpatterns = patterns('',
    url(r'^admin_tools/', include('admin_tools.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^', include('panov.urls')),

    # static files
    (r'^assets/admin_tools/(?P<path>.*)$', 'django.views.static.serve',
     {'document_root': os.path.join(settings.DIRNAME,
                                    'panov', 'media', 'admin_tools')}),
    (r'^assets/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),
)
