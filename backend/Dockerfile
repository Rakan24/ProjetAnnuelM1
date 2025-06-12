# Utilise une image légère avec Python
FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de requirements (si tu les as)
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste du backend
COPY . .

# Lancer le serveur (déjà défini dans docker-compose)
