#!/bin/bash

python manage.py migrate &t
python manage.py runserver 0.0.0.0:8020
