from flask import Blueprint, request, jsonify
from app.services.tweet_service import analyze_tweets, fetch_tweets
from app.services.metrics_service import calculate_metrics 

tweet_blueprint = Blueprint("tweets", __name__)

@tweet_blueprint.route("/", methods=["POST"])
def post_tweets():
    try:
        data = request.get_json()

        if not isinstance(data, dict):
            raise ValueError("Le format de la requête est invalide. Un objet JSON est attendu.")

        tweets = data.get("tweets")

        if not isinstance(tweets, list) or not tweets:
            raise ValueError("La clé 'tweets' doit contenir une liste non vide.")

        if not all(isinstance(tweet, str) and tweet.strip() for tweet in tweets):
            raise ValueError("Tous les éléments de la liste 'tweets' doivent être des chaînes de caractères non vides.")

        result = analyze_tweets(tweets)

        return jsonify(result), 200

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400 
    except Exception as e:
        return jsonify({"error": f"Erreur interne : {str(e)}"}), 500 


@tweet_blueprint.route("/", methods=["GET"])
def get_tweets():
    try:
        result = fetch_tweets()

        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": f"Erreur interne : {str(e)}"}), 500 
    

@tweet_blueprint.route("/metrics", methods=["GET"])
def get_metrics():
    try:
        y_true = ['positif', 'négatif', 'positif', 'négatif', 'positif', 'positif', 'négatif']
        y_pred = ['positif', 'négatif', 'négatif', 'négatif', 'positif', 'positif', 'positif']

        metrics = calculate_metrics(y_true, y_pred)

        return jsonify(metrics), 200

    except Exception as e:
        return jsonify({"error": f"Erreur interne : {str(e)}"}), 500


@tweet_blueprint.route("/reinforcement", methods=["POST"])
def reinforcement_api():
    from app.services.reinforcement import push_new_datas
    try:
        data = request.get_json()
        if not data or "tweets" not in data:
            raise ValueError("Le JSON doit contenir une clé 'tweets'.")

        tweets = data["tweets"]

        if not isinstance(tweets, list):
            raise ValueError("'tweets' doit être une liste.")

        for tweet in tweets:
            if not isinstance(tweet, dict) or "text" not in tweet or "label" not in tweet:
                raise ValueError("Chaque tweet doit être un dictionnaire avec 'text' et 'label'.")

            if not isinstance(tweet["text"], str) or not isinstance(tweet["label"], int):
                raise ValueError("'text' doit être une chaîne et 'label' un entier.")

            if tweet["label"] not in [0, 1]:
                raise ValueError("Le label doit être 0 (positif) ou 1 (négatif).")

        push_new_datas(tweets)

        return jsonify({"message": "Données ajoutées."}), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400