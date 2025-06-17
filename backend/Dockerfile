# Utilise une image légère de Python
FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app

# Pré-installe les dépendances système nécessaires
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Copier les dépendances Python
COPY requirements.txt .
COPY wait_for_postgres.sh ./wait_for_postgres.sh
RUN chmod +x ./wait_for_postgres.sh

# Installer les dépendances
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copier le code du projet
COPY . .

# Port par défaut de Django (utile si tu testes sans docker-compose)
EXPOSE 8000

# Commande de démarrage (à définir dans docker-compose en général)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
