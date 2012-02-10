# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core import urlresolvers
from django.core.management import call_command
from django.core.urlresolvers import reverse
from django.db import models
from django_webtest import WebTest
from panov.models import Person, ContactInfo
from request.models import Request
from tddspry.django.cases import DatabaseTestCase, HttpTestCase
import datetime
import shlex
import subprocess


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

    def test_admin_edit_url(self):
        person = Person.objects.latest('id')
        obj = person
        self.go200('index')
        content_type = ContentType.objects.get_for_model(obj.__class__)
        admin_url = urlresolvers.reverse("admin:%s_%s_change" % \
                               (content_type.app_label,
                                content_type.model),
                                     args=(obj.id,))

        self.find(admin_url)

    def test_person_edit_url(self):
        person = Person.objects.latest('id')
        self.go200('index')
        person_edit_url = urlresolvers.reverse("person-edit",
                                               kwargs={
                                                       "person_id": person.id}
                                               )

        self.find(person_edit_url)


    def test_history_page_link(self): 
        self.go200('index')
        url = urlresolvers.reverse("history")
        self.find(url)


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
            self.find(str(req.time.strftime("%d %m %H:%M:%S")))
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
        from panov.context_processors import settings as context_settings

        factory = RequestFactory()
        request = factory.get('/')

        c = RequestContext(request, {'foo': 'bar'}, [context_settings])
        self.assertTrue('settings' in c)
        self.assertEquals(c['settings'], django_settings)


class ModelsCommandTest(DatabaseTestCase):

    def setUp(self):
        self.out_file = "tests_out.txt"
        self.error_file = "tests_error.txt"

    def tearDown(self):
        command = 'rm -f %s' % self.out_file
        args = shlex.split(command)
        subprocess.Popen(args)

        command = 'rm -f %s' % self.error_file
        args = shlex.split(command)
        subprocess.Popen(args)

    def test_command(self):
        from panov import models as p_models
        call_command('models', 'panov',)
        log = ' '.join(open(self.out_file, 'rt').readlines())
        error_log = ' '.join(open(self.error_file, 'rt').readlines())
        module_models = models.get_models(p_models)
        for model in module_models:

            expr = u' '.join([unicode(model),
                                   unicode(model.objects.count())]) in log
            self.assertTrue(expr)

            expr = 'error: ' + u' '.join([unicode(model),
                                unicode(model.objects.count())]) in error_log
            self.assertTrue(expr)


class ModelSignalTest(DatabaseTestCase):

    def test_create(self):
        person = Person.objects.create(name=u'name',
                                       last_name='last_name',
                                       )
        c = Person.history.filter(id=person.id,
                                  history_type=u'+').count()
        self.assertEquals(c, 1)

    def test_delete(self):
        person = Person.objects.create(name=u'name',
                                       last_name='last_name',
                                       )

        id = person.id
        person.delete()
        del person

        c = Person.history.filter(id=id,
                                  history_type=u'-').count()
        self.assertEquals(c, 1)

    def test_edit(self):
        person = Person.objects.create(name=u'name',
                                       last_name='last_name',
                                       )

        person.name = u'name1'
        person.save()

        c = Person.history.filter(id=person.id,
                                  history_type=u'~').count()
        self.assertEquals(c, 1)


class EditPersonFormTest(WebTest):

    def test_form(self):

        person = Person.objects.latest('id')
        response = self.app.get(reverse('person-edit',
                           kwargs={'person_id': person.id}))

        form = response.form

        person_data = {'name': u'test name',
                       'last_name': u'test name last_name',
                       'birthdate': u"1981-08-12",
                       'bio': u"test bio",
                       }

        for key, value in person_data.iteritems():
            form[key] = value

        ci_data = {"email": "email@test.com",
                   "jabber": "email@test.com",
                   "skype": "skype@test.com",
                   "other_contacts": "other info"}

        for key, value in ci_data.iteritems():
            key = 'contactinfo-0-' + key
            form[key] = value

        form.submit()
        person = Person.objects.latest('id')

        for key in ['name', 'last_name', 'bio']:
            self.assertEquals(getattr(person, key), person_data[key])
        self.assertEquals(person.birthdate, datetime.date(1981, 8, 12))

        ci = person.contactinfo

        for key, value in ci_data.iteritems():
            self.assertEquals(getattr(ci, key), value)


class HistoryPageTest(HttpTestCase):

    def test_page(self):
        self.go200("history")
        module_models = [Person, ContactInfo]

        for model in module_models:
            history = model.history.all()
            for record in history:
                self.find(record.history_date.strftime("%d %m %Y %H:%M:%S"))
                self.find(unicode(record.history_object))
                self.find(record.get_history_type_display())
                self.find(unicode(record.changed_by))
