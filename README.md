# dokudog-main

This is the main repo for Project Dokudog. It is a Django App that hosts the main framework for the Dokudog App.
The app relies on two other GitHub Repos to function. It uses a dokudog-reccomendation app to get reccomendations 
and it uses the dokudog-grading app to grade the difficulty of works.

The reccomendation query framework is currently a RESTful API, while the grading system is using Redis and Celery.
The RESTful API is its own Django app, while Redis and Celery are currently run via Docker. 
