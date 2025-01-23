# **Project-Algo-FLMP**

Un projet d'école.

## **Installer le projet**

Pour démarrer le projet, suivez les étapes suivantes :

1. **Créer et activer un environnement virtuel :**

```sh
python -m venv venv

# Linux :
source venv/bin/activate

# ou Windows :
venv\Scripts\activate
```

2. **Installer les dépendances :**

```sh
pip install -r requirements.txt
```

---

## **Lancer le projet**

Pour exécuter l'application FastAPI, utilisez la commande suivante :  
```sh
fastapi dev app/main.py
```

L'application sera disponible à l'adresse que FastAPI affichera dans la console (par défaut sur [http://127.0.0.1:8000](http://127.0.0.1:8000)).

---

### **Lancer la base de données**

1. Démarrez les conteneurs Docker :  
   ```sh
   docker compose up -d
   ```

2. Accédez à **phpMyAdmin** :  
   - URL : [http://localhost:8080](http://localhost:8080)  
   - Identifiants de connexion :  
     - **Utilisateur** : `root`  
     - **Mot de passe** : `password`  

