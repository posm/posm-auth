#! /bin/sh

python3 /code/manage.py collectstatic --no-input &
python3 /code/manage.py migrate --no-input

uwsgi --ini /code/deploy/configs/uwsgi.ini # Start uwsgi wv_dvs
