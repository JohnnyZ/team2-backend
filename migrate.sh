#!/bin/bash
./manage.py makemigrations
sudo git add -A
sudo git commit -m "generic push"
sudo git push heroku
sudo heroku run python manage.py migrate
