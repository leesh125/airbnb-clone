#!/bin/bash

source /var/app/venv/*/bin/activate
cd /var/app/staging

python manage.py seed_users --number 50
python manage.py seed_amenities 
python manage.py seed_facilities 
python manage.py seed_rooms --number 100
python manage.py seed_reviews --number 200
python manage.py seed_reservations --number 20