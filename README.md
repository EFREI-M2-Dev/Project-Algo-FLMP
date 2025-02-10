# **Project-Algo-FLMP**

## **Installer le projet**

Le projet est configuré pour fonctionner directement avec Docker, il n'est pas nécessaire d'utiliser un environnement virtuel ou d'installer manuellement les dépendances. Suivez les étapes ci-dessous pour démarrer le projet dans un environnement Docker.

---

## **Lancer le projet avec Docker**

### 1. **Démarrer les services Docker :**

Depuis le répertoire du projet, exécute la commande suivante pour démarrer tous les services Docker (Flask, MySQL, et phpMyAdmin) :

```sh
docker compose up --build -d
```

Cela va :

-   Construire et démarrer le conteneur Flask (`flask-app`)
-   Démarrer le conteneur MySQL (`mysql`)
-   Démarrer le conteneur phpMyAdmin (`phpmyadmin`)

### 2. **Accéder à l'application Flask :**

Une fois les services démarrés, l'application Flask sera accessible sur l'URL suivante :  
[http://localhost:5001](http://localhost:5001) (Cela redirige vers le port 5000 du conteneur Flask).

### 3. **Accéder à phpMyAdmin :**

phpMyAdmin est également disponible pour gérer la base de données MySQL via une interface web.

-   URL : [http://localhost:8080](http://localhost:8080)
-   Identifiants de connexion :
    -   **Utilisateur** : `root`
    -   **Mot de passe** : `rootpassword`

---

### **Démarrer la base de données MySQL avec Docker :**

1. Les services MySQL et phpMyAdmin démarrent automatiquement avec Docker, donc pas besoin de les configurer manuellement.

2. Si tu souhaites t'assurer que MySQL est bien en fonctionnement, tu peux vérifier en accédant à [phpMyAdmin](http://localhost:8080).

---

## **Arrêter le projet**

Pour arrêter les services Docker, exécute la commande suivante :

```sh
docker compose down -v
```

Cela arrêtera et supprimera les conteneurs, les réseaux et les volumes associés.

Pour garder les volumes intactes, préferez la commande suivante:

```sh
docker compose down
```

# Endpoints de l'API

## 1. Envoyer des tweets (`POST /tweets/`)

### **Description**

Cet endpoint permet d'envoyer une liste de tweets à analyser.

### **Requête**

```sh
curl -X POST http://localhost:5001/tweets/ \
     -H "Content-Type: application/json" \
     -d '{
           "tweets": [
             "Quel contenu inspirant ce livre",
             "Ecoute et ferme-la !"
           ]
         }'
```

### **Réponse (Exemple)**

```json
{
    "Ecoute et ferme-la !": -0.33,
    "Quel contenu inspirant ce livre": 0.39
}
```

---

## 2. Récupérer les tweets analysés (`GET /tweets/`)

### **Description**

Cet endpoint retourne la liste des tweets analysés avec leurs scores de sentiment.

### **Requête**

```sh
curl -X GET http://localhost:5001/tweets/
```

### **Réponse (Exemple)**

```json
{
    "1": {
        "ID": 1,
        "negative": 0,
        "positive": 1,
        "text": "J'ai beaucoup apprécié cette lecture, très enrichissante."
    }
}
```
