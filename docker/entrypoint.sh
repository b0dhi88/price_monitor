#!/bin/sh

echo "Waiting for Redis..."
until redis-cli -h redis ping > /dev/null 2>&1; do
    echo "Redis is unavailable - sleeping"
    sleep 2
done
echo "Redis is up!"

echo "Running migrations..."
python manage.py migrate --noinput

echo "Starting Django server..."
exec "$@"
