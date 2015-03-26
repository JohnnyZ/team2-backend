#!/bin/bash
pip freeze > requirements.txt
sudo git add -A
echo 'Enter the git commit message for backend.. ONLY'
read gitcommit
sudo git commit -m "$gitcommit"
sudo git push backend
