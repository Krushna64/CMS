# Content Management System (Django Application)

## Setup

Clone the repository:

```sh
$ git clone https://github.com/Krushna64/CMS.git
$ cd sample-django-app
```

Create a virtual environment to install dependencies in and activate it:

```sh
$ python -m venv venv
$ source venv/bin/activate
```

Install dependencies:

```sh
(venv)$ pip install -r requirements.txt
```

Run migrations:
```sh
(venv)$ python manage.py makemigrations api
(venv)$ python manage.py migrate
```

Create a superuser (for admin access):
```
(venv)$ python manage.py createsuperuser
```

Run the server:
```
(venv)$ python manage.py runserver
```

And navigate to `http://127.0.0.1:8000/`.

## Tests

To run the tests, `cd` into the directory where `manage.py` is:
```sh
(venv)$ python manage.py test api
```

## Coverage

```sh
(venv)$ coverage run --source='.' manage.py test api
(venv)$ coverage html -d coverage
```

Open coverage/index.html in a browser to view the coverage report.