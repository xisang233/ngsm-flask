gunicorn -D -w 2 -b 0.0.0.0:5000 flask_app:app
