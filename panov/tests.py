# -*- coding: utf-8 -*-
from tddspry.django.cases import DatabaseTestCase, HttpTestCase
from panov.models import Person, ContactInfo


class AdminUserTest(HttpTestCase):
    '''
    test for admin
    '''
    fixtures = ['initial_data.json']

    USERNAME = 'admin'
    PASSWORD = 'admin'

    def test_admin_credentials(self):

        self.login_to_admin(self.USERNAME, self.PASSWORD)


class MainPageTest(HttpTestCase):

    fixtures = ['initial_data.json']

    def test_main_page(self):
        person = Person.objects.latest('id')
        self.go200('index')
        self.find(str(person.name))
        self.find(str(person.last_name))
        self.find(str(person.birthdate.strftime("%d.%m.%Y")))
        self.find(str(person.bio))
        self.find(str(person.contactinfo.email))
        self.find(str(person.contactinfo.jabber))
        self.find(str(person.contactinfo.skype))


class RequestTest(HttpTestCase):

    fixtures = ['initial_data.json']

    def test_request_list_page(self):
        self.go200('request-list')


class PersonTest(DatabaseTestCase):

    def setUp(self):

        self.person = Person.objects.create(name=u'name',
                                           last_name='last_name',
                                           )

    def tearDown(self):
        self.person.delete()

    def test_unicode(self):

        person = self.person
        self.assertEqual(unicode(self.person),
                         u' '.join([person.name, person.last_name]))


class ContactInfoTest(DatabaseTestCase):

    def setUp(self):

        self.person = Person.objects.create(name=u'name',
                                           last_name='last_name',
                                           )
        self.ci = ContactInfo.objects.create(owner=self.person)

    def test_unicode(self):

        person = self.ci.owner
        right_value = u' '.join([person.name, person.last_name, u'contacts'] )
        self.assertEqual(unicode(self.ci), right_value)
 