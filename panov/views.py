# -*- coding: utf-8 -*-
from panov.models import Person
from request.models import Request
from django.shortcuts import render


def index(request, template_name='index.html', extra_context={}):

    person = Person.objects.latest('id')

    context = {
               'person': person,
               'ci': person.contactinfo,
               }
    context.update(extra_context)
    return render(request, template_name, context)


def request_list(request, template_name='request_list.html', extra_context={}):

    default_limit = 10

    limit = request.GET.get('limit', default_limit)

    try:
        int(limit)
    except ValueError:
        limit = default_limit

    request_list = Request.objects.all()[:limit]

    context = {
               'request_list': request_list,
               }
    context.update(extra_context)
    return render(request, template_name, context)
