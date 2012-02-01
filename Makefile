all: test

test: 
	django-nosetests.py

coverage:
	 python manage.py test_coverage
