web: gunicorn cinewhisper.wsgi
worker: celery -A cinewhisper worker --loglevel=info
beat: celery -A cinewhisper beat --loglevel=info
