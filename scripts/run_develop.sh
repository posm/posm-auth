#!/bin/sh -x

python3 manage.py migrate --no-input
# Load component_permissions from fixtures
python3 manage.py loaddata component_permissions

python3 manage.py runserver 0.0.0.0:8050
