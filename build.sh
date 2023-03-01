#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements-dev.txt

python ./src/manage.py collectstatic --no-input
python ./src/manage.py migrate --settings=setup.settings.prod

# python ./src/manage.py shell < src/seed.py --settings=setup.settings.prod
