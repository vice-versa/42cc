# -*- coding: utf-8 -*-
from panov.models import Person
from request.models import Request
from django.conf import settings

from django.shortcuts import render
from django.forms.models import modelform_factory


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


def person_edit(request, person_id, template_name='person_edit.html',
                extra_context={}):
    form = modelform_factory(Person)
    context = {
               'form': form,
               }
    context.update(extra_context)
    return render(request, template_name, context)

