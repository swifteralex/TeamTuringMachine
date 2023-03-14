@ECHO OFF

ECHO Starting virtual environment...
cd django-env-win/Scripts
call activate.bat

ECHO Ensuring pip is installed...
py -m ensurepip

ECHO Installing Django...
py -m pip install Django

ECHO Running server...
cd ../../titanic
start msedge --new-window http://127.0.0.1:8000/ship
py manage.py runserver

PAUSE