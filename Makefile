PORT ?= 8000
WEB_CONCURRENCY ?= 4

install:
	poetry install

dev:
	poetry run python task_manager/manage.py runserver

start:
	poetry run gunicorn task_manager.wsgi:application
