from panov.models import ContactInfo, Person, OrderedRequest
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


class OrderedRequestAdminInline(admin.TabularInline):
    model = OrderedRequest
    extra = 0


class OrderedRequestAdmin(RequestAdmin):

    inlines = [OrderedRequestAdminInline, ]

admin.site.unregister(Request)
admin.site.register(Request, OrderedRequestAdmin)