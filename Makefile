migrate:
	python src/manage.py makemigrations --settings=setup.settings.local
	python src/manage.py migrate --settings=setup.settings.local

test:
	python src/manage.py test --failfast --settings=setup.settings.local
