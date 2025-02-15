#!/bin/bash

# Démarrer cron en arrière-plan
cron

# Exécuter les services Python
python -m app.services.init_service
python -m app.services.train_service
python -m app.main