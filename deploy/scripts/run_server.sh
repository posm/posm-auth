#! /bin/sh

python3 /code/manage.py collectstatic --no-input &

python3 /code/manage.py migrate --no-input
# Load component_permissions from fixtures
python3 manage.py loaddata component_permissions

uwsgi --ini /code/deploy/configs/uwsgi.ini --static-map /static=/static
