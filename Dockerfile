FROM python:3.10-slim

# Installer les dépendances système requises
RUN apt-get update && \
    apt-get install -y \
    pkg-config \
    default-libmysqlclient-dev \
    build-essential

# Créer un répertoire pour l'application
WORKDIR /app

# Copier les fichiers de l'application
COPY . /app

# Installer les dépendances Python
RUN pip install -r requirements.txt

# Commande pour démarrer l'application
CMD ["sh", "-c", "python -m app.services.train_service && python -m app.main"]

