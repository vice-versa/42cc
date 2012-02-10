# -*- coding: utf-8 -*-
<<<<<<< HEAD
from panov.models import Person, ContactInfo
=======
>>>>>>> t10_signal_processor
from request.models import Request
from django.conf import settings

from django.shortcuts import render
<<<<<<< HEAD
from django.forms.models import modelform_factory, inlineformset_factory
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login as generic_login
from django.contrib.auth import logout as auth_logout
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
=======
from panov.models import ContactInfo, Person
>>>>>>> t10_signal_processor


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


@login_required
def person_edit(request, person_id, template_name='person_edit.html',
                extra_context={}):

    person = Person.objects.get(id=person_id)
    person_form = modelform_factory(Person)
    contact_info_form = inlineformset_factory(Person, ContactInfo,
                                              can_delete=False)

    if request.method == "POST":
        data = request.POST
        person_form = person_form(data=data,
                                  instance=person)
        contact_info_form = contact_info_form(data=data,
                                              instance=person.contactinfo)
        if person_form.is_valid():
            person_form.save()
        if contact_info_form.is_valid():
            contact_info_form.save()
    else:
        person_form = person_form(instance=person)
        contact_info_form = contact_info_form(instance=person.contactinfo)
    context = {
               'person_form': person_form,
               'contact_info_form': contact_info_form,
               }
    context.update(extra_context)
    return render(request, template_name, context)

login = generic_login


def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse('index'))


def history(request, template_name='history.html', extra_context={}):

    module_models = [Person, ContactInfo]

    context = {
               'module_models': []
               }

    for model in module_models:
        context['module_models'].append(
                                        {str(model): list(model.history.all())})

    context.update(extra_context)
    return render(request, template_name, context)

