#!/bin/bash

echo "Waiting for MySQL..."
while ! nc -z db 3306; do
  sleep 0.5
done
echo "MySQL started"

if [ "$RUN_MAIN" = "true" ] && [ "$SERVICE" = "django" ]; then
  echo "Applying migrations..."
  python manage.py migrate
fi

case "$SERVICE" in
  django)
    exec python manage.py runserver 0.0.0.0:8000
    ;;
  celery_worker)
    exec celery -A hopeconnect worker --loglevel=info
    ;;
  celery_beat)
    exec celery -A hopeconnect beat --loglevel=info
    ;;
  *)
    echo "Unknown service: $SERVICE"
    exit 1
    ;;
esac
