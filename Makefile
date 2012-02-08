all: test

test: 
	django-nosetests.py

coverage:
	python manage.py test_coverage

runserver:
	python manage.py runserver 8080
     
syncdb:
	python manage.py syncdb
shell:
	python manage.py shell
