#!/bin/sh

# tells the bash shell to exit immediately if any subsequent commands returns a non-zero (error) exit status
set -e

# apply database migrations
python manage.py migrate --noinput

# start server
gunicorn prowlscan.asgi:application --bind 0.0.0.0 -k uvicorn_worker.UvicornWorker \
    --workers 4 --log-file -
