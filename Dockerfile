FROM python:3.10-slim

# Installer les dépendances système requises
RUN apt-get update && \
    apt-get install -y \
    pkg-config \
    default-libmysqlclient-dev \
    build-essential \
    cron && \
    rm -rf /var/lib/apt/lists/*

# Créer un répertoire pour l'application
WORKDIR /app

# Copier les fichiers de l'application
COPY . /app

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier le fichier crontab et lui donner les permissions adéquates
COPY cronjob /etc/cron.d/my-cron
RUN chmod 0644 /etc/cron.d/my-cron

# Ajouter le script d'entrée
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Utiliser le script d'entrée comme point de départ
CMD ["/entrypoint.sh"]