web: gunicorn backend.wsgi --bind 0.0.0.0:$PORT
websocket: daphne -b 0.0.0.0 -p $PORT backend.asgi:application

