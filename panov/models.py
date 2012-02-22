# -*- coding: utf-8 -*-
from django.db import models
from simple_history.models import HistoricalRecords
from django.db.models.signals import post_save
from request.models import Request
from django.db.models.base import ModelBase


class Person(models.Model):

    name = models.CharField(verbose_name=u'Name', max_length=255)
    last_name = models.CharField(verbose_name=u'Last Name', max_length=255)
    birthdate = models.DateField(verbose_name=u'Date of birth',
                                 null=True, blank=True)

    photo = models.ImageField(verbose_name=u'Photo',
                              upload_to='images/uploads/',
                              null=True, blank=True)

    bio = models.TextField(verbose_name=u'BIO', max_length=255,
                           null=True, blank=True)

    history = HistoricalRecords()

    def __unicode__(self):
        return u' '.join([self.name, self.last_name])


class ContactInfo(models.Model):

    owner = models.OneToOneField('panov.Person')

    email = models.EmailField(verbose_name=u'Email',
                              null=True, blank=True)

    jabber = models.CharField(verbose_name=u'JabberID', max_length=255,
                              null=True, blank=True)

    skype = models.CharField(verbose_name=u'SkypeID', max_length=255,
                             null=True, blank=True)

    other_contacts = models.TextField(verbose_name=u'Other Contacts',
                                      max_length=255,
                                      null=True, blank=True)

    def __unicode__(self):
        return u' '.join([self.owner.name, self.owner.last_name, u'contacts'])

    history = HistoricalRecords()


class TmpFile(models.Model):

    photo = models.ImageField(verbose_name=u'TmpPhoto',
                              upload_to='images/uploads/tmp/')

    history = HistoricalRecords()

    def __unicode__(self):
        return unicode(self.photo)


class _RequestExtensionModelBase(ModelBase):
    # _prepare is not part of the public API and may change

    def _prepare(cls):
        super(_RequestExtensionModelBase, cls)._prepare()

        def add_extension(sender, instance, created, **kwargs):
            if created:
                cls.objects.create(request=instance)

        # Automatically link extension when a new request is created
        post_save.connect(add_extension, sender=Request, weak=False)


class RequestExtensionModel(models.Model):

    __metaclass__ = _RequestExtensionModelBase

    request = models.OneToOneField('request.Request',
                                   verbose_name=u'Request',
                                   primary_key=True, parent_link=True
                                   )

    class Meta:
        abstract = True


class RequestExtension(RequestExtensionModel):

    position = models.IntegerField(verbose_name=u'position', default=0)

    def __unicode__(self):
        return u"%s %s" % (unicode(self.request), unicode(self.position))

    class Meta:

        verbose_name = u'Request extension'
        verbose_name_plural = u'Request extensions'
