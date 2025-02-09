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
