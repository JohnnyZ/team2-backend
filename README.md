# Getting Started

Create virtual environment in the folder

Run the following command to get the same version of python and django toolbelt etc
`pip install -r /path/to/requirements.txt`

Get Heroku Toolbelt stuff and run the following to be able to push to heroku
`heroku git:remote -a secure-headland-8362`

Then connect to the other git hub
`git remote add backend https://github.com/johnnyz/team2-backend.git`

# Files

apiusage.txt
---
Explains what apis are available and what a sample requests/response might look like

push.sh
---
Pushes to both heroku and the team2-backend git repos. It prompts for commit message. It's run with
`./push`

migrate.sh
---
Script to run whenever changing anything in the models file (or anything that changes database formation)

constants.py
---
All the constants for python scripts

models.py
---
The models that the database is created from

admin.py
---
The file responsible for formatting the admin panel

api.py
---
All the api code
