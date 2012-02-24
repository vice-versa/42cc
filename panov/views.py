# -*- coding: utf-8 -*-
from panov.models import Person, ContactInfo, TmpFile, RequestExtension
from request.models import Request
from django.conf import settings

from django.shortcuts import render
from django.forms.models import modelform_factory, inlineformset_factory
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login as generic_login
from django.contrib.auth import logout as auth_logout
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.forms.formsets import all_valid
from panov.forms import PersonForm, RequestExtensionForm
from django.template.loader import render_to_string
from django.utils import simplejson
from django.views.generic.base import View
from django.utils.decorators import method_decorator
from django.core.exceptions import FieldError


def index(request, template_name='index.html', extra_context={}):

    person = Person.objects.latest('id')
    context = {
               'person': person,
               'ci': person.contactinfo,
               }
    context.update(extra_context)
    return render(request, template_name, context)


class RequestListView(View):

    def get_context(self, request, form_extra={}, extra_context={}):

        limit = settings.REQUEST_LIST_PAGE_LIMIT
        order_by = settings.REQUEST_LIST_PAGE_ORDER_BY

        request_list = list(Request.objects.all().order_by(order_by))

        request_list = request_list[:limit]

        form_kwargs = {}

        for request in request_list:
            form = modelform_factory(RequestExtension, form=RequestExtensionForm)
            form_kwargs.update({
                                'instance': request.requestextension,
                                'initial': {'request_id': request.id
                                            }
                                })

            form = form(**form_kwargs)
            setattr(request, 'form', form)

        context = {
                   'request_list': request_list,
                   }
        context.update(extra_context)
        return context

    def get(self, request, template_name='request_list.html', extra_context={}):

        context = self.get_context(request, extra_context=extra_context)
        return render(request, template_name, context)

    def post_submit(self, request, template_name='request_list.html', extra_context={}):
        form_extra = {'data': request.POST}
        self.save_priority(request, form_extra)
        context = self.get_context(request, form_extra=form_extra,
                                   extra_context=extra_context)

        return render(request, template_name, context)

    def post_ajax(self, request, template_name='request_list.html',
                        extra_context={}):
        form_extra = {'data': request.POST}
        form = self.save_priority(request, form_extra)
        context = self.get_context(request, form_extra=form_extra,
                                   extra_context=extra_context)

        request_list_inline = render_to_string('request_list_inline.html',
                                               context)
        data = {
                'request_list': request_list_inline,
                }
        return HttpResponse(simplejson.dumps(data))

    def post(self, request, template_name='request_list.html', extra_context={}):

        if request.is_ajax():
            return self.post_ajax(request, template_name, extra_context)
        else:
            return self.post_submit(request, template_name, extra_context)

    def save_priority(self, request, form_extra):

        form = modelform_factory(RequestExtension, form=RequestExtensionForm)
        form_instance = form(**form_extra)
        if form_instance.is_valid():
            req_id = form_instance.cleaned_data['request_id']

        req = Request.objects.get(id=req_id)
        form_extra.update({'instance': req.requestextension})
        form_instance = form(**form_extra)
        if form_instance.is_valid():
            form_instance.save()

        return form


class PersonEditView(View):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PersonEditView, self).dispatch(*args, **kwargs)

    def get_forms(self):

        person_form = modelform_factory(Person, form=PersonForm)
        contact_info_form = inlineformset_factory(Person, ContactInfo,
                                                  can_delete=False)
        return person_form, contact_info_form

    def get_context(self, person_id, extra_form_args={}, extra_context={}):

        person = Person.objects.get(id=person_id)
        person_form, contact_info_form = self.get_forms()

        form_args = {'instance': person}
        form_args.update(extra_form_args)

        person_form = person_form(**form_args)

        form_args.update({'instance': person.contactinfo})
        contact_info_form = contact_info_form(**form_args)

        context = {
               'person_form': person_form,
               'contact_info_form': contact_info_form,
               'person': person,
               }
        context.update(extra_context)
        return context

    def get(self, request, person_id, template_name='person_edit.html',
                extra_context={}):

        context = self.get_context(person_id, extra_context=extra_context)
        return render(request, template_name, context)

    def post(self, request, person_id=None,
                    template_name='person_edit.html',
                    extra_context={}):

        extra_form_args = {'data': request.POST,
                           'files': request.FILES}

        if request.is_ajax():
            person_id = request.POST.get('person_id', 1)
            return self.post_ajax_submit(request, person_id=person_id,
                                         extra_form_args=extra_form_args,
                                         extra_context=extra_context)
        else:
            return self.post_submit(request, person_id=person_id,
                                   extra_form_args=extra_form_args,
                                   extra_context=extra_context)

    def post_submit(self, request, person_id,
                    extra_form_args={},
                    template_name='person_edit.html',
                    extra_context={}):

        context = self.get_context(person_id=person_id,
                                   extra_form_args=extra_form_args,
                                   extra_context=extra_context)

        person_form = context['person_form']
        contact_info_form = context['contact_info_form']

        if person_form.is_valid():
            person_form.save()
        if contact_info_form.is_valid():
            contact_info_form.save()
        if all_valid([contact_info_form, person_form]):
            return HttpResponseRedirect(reverse('index'))
        return render(request, template_name, context)

    def post_ajax_submit(self, request, person_id,
                         extra_form_args={},
                         extra_context={}):

        try:
            person_id = int(person_id)
        except ValueError:
            raise Http404()

        context = {'errors': ''}

        form_context = self.get_context(person_id=person_id,
                                        extra_form_args=extra_form_args,
                                        extra_context=extra_context)

        person_form = form_context['person_form']
        contact_info_form = form_context['contact_info_form']

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
