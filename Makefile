PORT ?= 8000
WEB_CONCURRENCY ?= 4

install:
	poetry install

dev:
	poetry run python manage.py runserver

start:
	poetry run gunicorn -w $(WEB_CONCURRENCY) -b 0.0.0.0:$(PORT) task_manager.wsgi:application

shell:
	django-admin shell

tests:
	poetry run python3 manage.py test task_manager.tests

coverage:
	poetry run coverage run --source='.' manage.py test task_manager.tests && poetry run coverage xml

lint:
	poetry run flake8 task_manager

migrate:
	poetry run python manage.py makemigrations && poetry run python manage.py migrate
