# -*- coding: utf-8 -*-
from tddspry.django.cases import DatabaseTestCase, HttpTestCase
from panov.models import Person, ContactInfo
from request.models import Request
from django.conf import settings


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

    def setUp(self):

        limit = settings.REQUEST_LIST_PAGE_DEFAULT_LIMIT
        self.limit = limit
        Request.objects.create(path='/first', ip='127.0.0.1')

        [Request.objects.create(path='/' * i,
                                ip='127.0.0.1')
                         for i in xrange(1, limit)]
        Request.objects.create(path='/last', ip='127.0.0.1')

    def test_request_list_page(self):
        self.go200('request-list')
        req_list = Request.objects.all().order_by('time')[:self.limit]
        for req in req_list:
            self.find(str(req.time.strftime("%d %m %H:%M:%S.%f")))
            self.find(str(req.path))
            self.find(str(req.response))
            self.find(str(req.method))


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
        right_value = u' '.join([person.name, person.last_name, u'contacts'])
        self.assertEqual(unicode(self.ci), right_value)


class SettingsProcessorTest(HttpTestCase):

    def test_settings(self):
        from django.template import RequestContext
        from django.test.client import RequestFactory
        from django.conf import settings as django_settings
        from panov.context_processors import settings

        factory = RequestFactory()
        request = factory.get('/')

        c = RequestContext(request, {'foo': 'bar'}, [settings])
        self.assertTrue('settings' in c)
        self.assertEquals(c['settings'], django_settings) 
