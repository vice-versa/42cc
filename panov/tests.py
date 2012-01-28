# -*- coding: utf-8 -*-
from tddspry.django.cases import DatabaseTestCase
from django.contrib.auth.models import User


class AdminUserTest(DatabaseTestCase):
    
    fixtures = ['initial_data.json',]
    
    USERNAME = 'admin'
    PASSWORD = 'sha1$c2ee8$533fa92410c831c7420cfc0f3c5b14ca2f0a7dc0'
    
    def test_admin_credentials(self):
        
        admin = User.objects.get(username=self.USERNAME,
                                 is_superuser=True,
                                 is_active=True)
        
        self.assert_equal(admin.username, self.USERNAME)
        self.assert_equal(admin.password, self.PASSWORD)
    