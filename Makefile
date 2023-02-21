migrate:
	python src/manage.py makemigrations --settings=setup.settings.local
	python src/manage.py migrate --settings=setup.settings.local

seed:
	make migrate
	python src/manage.py shell < src/seed.py --settings=setup.settings.local

test:
	python src/manage.py test --failfast --settings=setup.settings.local
