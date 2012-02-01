# -*- coding: utf-8 -*-
from django.db import models

       
class Person(models.Model):
    
    name = models.CharField(verbose_name=u'Name', max_length=255)
    last_name = models.CharField(verbose_name=u'Last Name', max_length=255)
    
    birthdate = models.DateField(verbose_name=u'Date of birth')
    
    bio = models.TextField(verbose_name=u'BIO', max_length=255,
                           null=True, blank=True)
    
    def __unicode__(self):
        return u' '.join([self.name, self.last_name])
    
    
class ContactInfo(models.Model):
    
    owner = models.OneToOneField('panov.Person')
    
    email = models.EmailField(verbose_name=u'Email',
                              null=True, blank=True)
    
    jabber = models.CharField(verbose_name=u'JabberID', max_length=255)
    
    skype = models.CharField(verbose_name=u'SkypeID', max_length=255)
    
    other_contacts = models.TextField(verbose_name=u'Other Contacts', max_length=255,
                           null=True, blank=True)

    def __unicode__(self):
        return u' '.join([self.owner.name, self.owner.last_name, u'contacts'] )
    