web: gunicorn cinewhisper.wsgi
web: celery -A cinewhisper worker --loglevel=info & celery -A cinewhisper beat --loglevel=info & python manage.py migrate && gunicorn cinewhisper.wsgi
