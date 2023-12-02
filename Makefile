PORT ?= 8000

dev:
	poetry run python manage.py runserver

start:
	poetry run gunicorn -w $(WEB_CONCURRENCY) -b 0.0.0.0:$(PORT) task_manager.wsgi:application