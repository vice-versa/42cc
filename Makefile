all: test

test: 
	django-nosetests.py

coverage:
	 python manage.py test_coverage

syncdb:
     python manage.py syncdb

runserver:
     python manage.py runserver 8080
	 