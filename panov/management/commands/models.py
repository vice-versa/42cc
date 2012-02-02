# -*- coding: utf-8 -*-

from django.core.management.base import LabelCommand
from django.db import models
from django.utils.log import getLogger


class Command(LabelCommand):

    def handle_label(self, label, **options):
        """
        Prints count of of objects of each model for app == label
        """
        module = __import__(label)
        module_models = models.get_models(getattr(module, 'models'))
        
        logger = getLogger('')
        
        for model in module_models:
            logger.info(u' '.join([unicode(model),
                                   unicode(model.objects.count())]))
