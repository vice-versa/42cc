from panov.models import ContactInfo, Person
from django.contrib import admin


class ContactInfoAdmin(admin.TabularInline):
    model = ContactInfo
    extra = 0
    
class PersonAdmin(admin.ModelAdmin):
    
    inlines = [ContactInfoAdmin, ]
    

admin.site.register(Person, PersonAdmin)
