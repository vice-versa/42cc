# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from tddspry.django.cases import DatabaseTestCase, HttpTestCase
from panov.models import Person, ContactInfo


class AdminUserTest(DatabaseTestCase):
    '''
    test for admin
    '''
    fixtures = ['initial_data.json']

    USERNAME = 'admin'
    PASSWORD = 'sha1$c2ee8$533fa92410c831c7420cfc0f3c5b14ca2f0a7dc0'

    def test_admin_credentials(self):

        admin = User.objects.get(username=self.USERNAME,
                                 is_superuser=True,
                                 is_active=True)

        self.assert_equal(admin.username, self.USERNAME)
        self.assert_equal(admin.password, self.PASSWORD)


class TestMainPage(HttpTestCase):

    fixtures = ['initial_data.json']

    def test_main_page(self):
        self.go200('index')


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

    def tearDown(self):
        self.person.delete()

    def test_unicode(self):

        person = self.ci.owner
        right_value = u' '.join([person.name, person.last_name, u'contacts'] )
        self.assertEqual(unicode(self.ci), right_value)
 