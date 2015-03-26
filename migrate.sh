#!/bin/bash
./manage.py makemigrations
sudo git add -A
echo 'Enter migration commit message for heroku and backend'
read gitcommit 
sudo git commit -m "$gitcommit"
sudo git push heroku
sudo heroku run python manage.py migrate
