# CSIS-658


This an implementation of the Simple ATM project in Paul C. Jorgensen's book ***Software Testing: A Craftsman's Approach***.

The project was implemented using Django, SQLite database, JQuery, and Selenium for testing.

## Run the Project

To run this project clone the repo and install Django.  Below is a link to the Django download page and also the pip install command.

> https://www.djangoproject.com/download/
> 
> pip install Django==2.0.4

From here you move into the directory of the project at the location of manage.py. The command below will run the local server so that the application can be used:

> python manage.py runserver

Once the server is running the URL below will load the initial page:

> http://localhost:8000/atm/

Django also provides a default admin page that can be used to manipulate the database.  The admin page can be access at the below URL:

> http://localhost:8000/admin

The login information for the admin is username of "admin" and password of "password1!".  From the admin page you can edit or create a new user that can be used by the application.

## Test the Project

To run the tests in this project install Selenium for Python. Below is a link to the Selenium download page and also the pip install command.

> http://selenium-python.readthedocs.io/installation.html
> 
> pip install selenium

From here you move into the directory of the project at the location of manage.py. The command below will run all of the Selenium tests:

> python manage.py test

## View Code Coverage

To view code coverage click into the cover directory and open index.html. The test coverage is generated after each run of the tests. Code coverage is viewed with the use of django_nose. Below is a link to the django_nose download page and also the pip install command.

> https://django-nose.readthedocs.io/en/latest/installation.html
> 
> pip install django_nose




