# -*- coding: utf-8 -*-
from request.models import Request
from django.conf import settings

from django.shortcuts import render
from panov.models import ContactInfo, Person


def index(request, template_name='index.html', extra_context={}):

    person = Person.objects.latest('id')

    context = {
               'person': person,
               'ci': person.contactinfo,
               }
    context.update(extra_context)
    return render(request, template_name, context)


def request_list(request, template_name='request_list.html', extra_context={}):

    limit = request.GET.get('limit', settings.REQUEST_LIST_PAGE_DEFAULT_LIMIT)

    try:
        int(limit)
    except ValueError:
        pass

    request_list = Request.objects.all().order_by('time')[:limit]

    context = {
               'request_list': request_list,
               }
    context.update(extra_context)
    return render(request, template_name, context)


def history(request, template_name='history.html', extra_context={}):

    module_models = [Person, ContactInfo]

    context = {
               'module_models': []
               }

    for model in module_models:
        context['module_models'].append(
                                        {str(model):list(model.history.all())})

    context.update(extra_context)
    return render(request, template_name, context)


