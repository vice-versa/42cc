# -*- coding: utf-8 -*-
import sys
from django import conf
from django.conf import LazySettings


class SettingsProcessor(object):
    def __getattr__(self, attr):
        if attr == '__file__':
            # autoreload support in dev server
            return __file__
        else:
            return lambda request: {attr: getattr(conf, attr)}

sys.modules[__name__ + '.conf'] = SettingsProcessor()