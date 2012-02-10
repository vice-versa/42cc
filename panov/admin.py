from panov.models import ContactInfo, Person
from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin


class ContactInfoAdmin(admin.TabularInline):
    model = ContactInfo
    extra = 0


class PersonAdmin(SimpleHistoryAdmin):

    inlines = [ContactInfoAdmin, ]


admin.site.register(Person, PersonAdmin)
