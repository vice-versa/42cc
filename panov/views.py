# -*- coding: utf-8 -*-
from django.shortcuts import render
from panov.models import Person


def index(request):

    person = Person.objects.get(name=u'Sergey', last_name=u'Panov')

    context = {
               'person': person,
               'ci': person.contactinfo,
               }

    return render(request, 'index.html', context)
