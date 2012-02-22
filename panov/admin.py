from panov.models import ContactInfo, Person, RequestExtension
from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from request.admin import RequestAdmin
from request.models import Request


class ContactInfoAdmin(admin.TabularInline):
    model = ContactInfo
    extra = 0


class PersonAdmin(SimpleHistoryAdmin):

    inlines = [ContactInfoAdmin, ]


admin.site.register(Person, PersonAdmin)


class RequestExtensionAdminInline(admin.TabularInline):
    model = RequestExtension
    extra = 0
    can_delete = False


class RequestExtensionAdmin(RequestAdmin):

    inlines = [RequestExtensionAdminInline, ]

admin.site.unregister(Request)
admin.site.register(Request, RequestExtensionAdmin)
