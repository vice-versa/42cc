# -*- coding: utf-8 -*-
from panov.models import Person, ContactInfo, TmpFile
from request.models import Request
from django.conf import settings

from django.shortcuts import render, get_object_or_404
from django.forms.models import modelform_factory, inlineformset_factory
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login as generic_login
from django.contrib.auth import logout as auth_logout
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.forms.formsets import all_valid
from panov.forms import PersonForm
from django.template.loader import render_to_string
from django.utils import simplejson
from django.forms.util import ErrorDict
import time


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
    person_form = modelform_factory(Person, form=PersonForm)
    contact_info_form = inlineformset_factory(Person, ContactInfo,
                                              can_delete=False)

    if request.method == "POST":
        data = request.POST
        person_form = person_form(data=data, files=request.FILES,
                                  instance=person)
        contact_info_form = contact_info_form(data=data,
                                              instance=person.contactinfo)
        if person_form.is_valid():
            person_form.save()
        if contact_info_form.is_valid():
            contact_info_form.save()
        if all_valid([contact_info_form, person_form]):
            return HttpResponseRedirect(reverse('index'))
    else:
        person_form = person_form(instance=person)
        contact_info_form = contact_info_form(instance=person.contactinfo)
    context = {
               'person_form': person_form,
               'contact_info_form': contact_info_form,
               'person': person,
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


def upload(request, person_id):
    context = {'errors': ''}
    tmp_file_form = modelform_factory(TmpFile)
    tmp_file_form = tmp_file_form(data=request.POST, files=request.FILES)
    if tmp_file_form.is_valid():
        tmp_file = tmp_file_form.save()
        msg = render_to_string("photo_thumbnail.html",
                               {'photo': tmp_file.photo}
                               )
        context["msg"] = msg
    else:
        context['errors'] = tmp_file_form.errors['photo']
    return HttpResponse(simplejson.dumps(context))


def ajax_submit(request):
    time.sleep(5)
    if not request.is_ajax():
        raise Http404()

    if request.method == "POST":
        person_id = request.POST.get('person_id', 1)

        try:
            person_id = int(person_id)
        except ValueError:
            raise Http404()

        context = {'errors': ''}
        person = get_object_or_404(Person, id=person_id)
        person_form = modelform_factory(Person, form=PersonForm)
        contact_info_form = inlineformset_factory(Person, ContactInfo)

        data = request.POST
        person_form = person_form(data=data, files=request.FILES,
                                  instance=person)
        contact_info_form = contact_info_form(data=data,
                                              instance=person.contactinfo)
        if not person_form.is_valid():
            context['errors'] = []
            context["errors"].extend([(field_name, errors)
                                      for field_name, errors in person_form.errors.items()
                                     ])
        if not contact_info_form.is_valid():
            if not context['errors']:
                context['errors'] = []
            for form in contact_info_form.forms:
                context["errors"].extend([(form.prefix+ "-" + field_name, errors)
                                      for field_name, errors in form.errors.items()
                                     ])

        return HttpResponse(simplejson.dumps(context))
