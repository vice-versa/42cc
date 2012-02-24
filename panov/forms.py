# -*- coding: utf-8 -*-
from panov.models import Person, RequestExtension
from django.forms.models import ModelForm
from django.forms.fields import ImageField, DateField, IntegerField
from django.forms.widgets import ClearableFileInput, CheckboxInput, DateInput,\
    TextInput
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string


class PhotoWidget(ClearableFileInput):

    template_with_initial = u'%(input)s <br/ >%(initial)s<br />%(clear_template)s <br />'

    template_with_clear = u'<div class="left">%(clear)s <label for="%(clear_checkbox_id)s">%(clear_checkbox_label)s</label></div>'

    def render(self, name, value, attrs=None):
        substitutions = {
            'input_text': self.input_text,
            'clear_template': '',
            'clear_checkbox_label': self.clear_checkbox_label,
        }

        template = u'%(input)s <br/ ><div class="preview"></div>'
        substitutions['input'] = super(ClearableFileInput, self).render(name,
                                                                        value,
                                                                        attrs)
        if value and hasattr(value, "url"):
            template = self.template_with_initial
            substitutions['initial'] = render_to_string("photo_thumbnail.html",
                                                    {'photo': value})
            if not self.is_required:
                checkbox_name = self.clear_checkbox_name(name)
                checkbox_id = self.clear_checkbox_id(checkbox_name)
                substitutions['clear_checkbox_name'] = conditional_escape(checkbox_name)
                substitutions['clear_checkbox_id'] = conditional_escape(checkbox_id)
                substitutions['clear'] = CheckboxInput().render(checkbox_name,
                                                                False,
                                                                attrs={'id': checkbox_id})
                substitutions['clear_template'] = self.template_with_clear % substitutions

        return mark_safe(template % substitutions)


class PhotoField(ImageField):
    widget = PhotoWidget


class CalendarWidget(DateInput):
    def __init__(self, attrs={}, format=None):
        attrs['class'] = attrs.get('class', '') + " " + 'calendar'
        super(CalendarWidget, self).__init__(attrs=attrs, format=format)


class CalendarForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(CalendarForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field, DateField):
                attrs = field.widget.attrs.copy()
                format = field.widget.format
                field.widget = CalendarWidget(attrs=attrs, format=format)


class PersonForm(CalendarForm):
    model = Person

    photo = PhotoField(label=u"Photo", required=False)


class RequestExtensionForm(ModelForm):
    model = RequestExtension

    request_id = IntegerField(required=True,
                              widget=TextInput(attrs={'style': "display:None"})
                              )

