web: gunicorn post_proj.wsgi:application --log-file - --log-level debug
python manage.py collectstatic --noinput

release: python manage.py migrate