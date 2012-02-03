# -*- coding: utf-8 -*-
from django import template
from django.core import urlresolvers
from django.contrib.contenttypes.models import ContentType

register = template.Library()


@register.inclusion_tag('admin_url.html')
def admin_url(obj):
    content_type = ContentType.objects.get_for_model(obj.__class__)
    admin_url = urlresolvers.reverse("admin:%s_%s_change" % \
                               (content_type.app_label,
                                content_type.model),
                                     args=(obj.id,))
    return {'admin_url': admin_url}
