# -*- coding: utf-8 -*-
from django.shortcuts import render
from panov.models import Person


def index(request, template_name='index.html'):

    person = Person.objects.latest('id')

    context = {
               'person': person,
               'ci': person.contactinfo,
               }

    return render(request, template_name, context)
