web: celery -A cinewhisper worker --loglevel=info & celery -A cinewhisper beat --loglevel=info & python manage.py migrate && python manage.py collectstatic --no-input && gunicorn cinewhisper.wsgi
