# -*- coding: utf-8 -*-
from panov.models import Person
from django.forms.models import ModelForm
from django.forms.fields import ImageField
from django.forms.widgets import ClearableFileInput, CheckboxInput
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string


class PhotoWidget(ClearableFileInput):

    template_with_initial = u'%(input_text)s: %(input)s <br/ >%(clear_template)s <br />%(initial)s <br />'

    template_with_clear = u'%(clear)s <label for="%(clear_checkbox_id)s">%(clear_checkbox_label)s</label>'

    def render(self, name, value, attrs=None):
        substitutions = {
            'input_text': self.input_text,
            'clear_template': '',
            'clear_checkbox_label': self.clear_checkbox_label,
        }
        template = u'%(input)s'
        substitutions['input'] = super(ClearableFileInput, self).render(name, value, attrs)

        if value and hasattr(value, "url"):
            template = self.template_with_initial
            substitutions['initial'] = render_to_string("photo_thumbnail.html", {'photo':value})
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


class PersonForm(ModelForm):
    model = Person

    photo = PhotoField(label=u"Photo")
