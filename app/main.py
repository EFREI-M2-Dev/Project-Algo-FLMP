from app import create_app
from app.scheduler import start_scheduler

app = create_app()

if __name__ == "__main__":
    # Démarrer le planificateur
    start_scheduler()
    
    # Lancer l'application Flask
    app.run(host='0.0.0.0', port=5000)
