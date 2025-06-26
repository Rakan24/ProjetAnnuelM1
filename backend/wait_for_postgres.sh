#!/bin/sh

while ! nc -z db 5432; do
  echo "⏳ Attente de la base de données à db:5432..."
  sleep 1
done

echo "✅ Base de données disponible, lancement des migrations..."
python manage.py migrate

echo "✅ Migrations appliquées, lancement du serveur Django..."
exec "$@"
