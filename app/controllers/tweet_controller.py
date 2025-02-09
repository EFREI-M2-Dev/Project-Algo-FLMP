from flask import Blueprint, request, jsonify
from app.services.tweet_service import analyze_tweets
from app.services.metrics_service import calculate_metrics 
from app.config.db import mysql

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

        cursor = mysql.connection.cursor()
        for tweet in tweets:
            score = result.get(tweet, 0)
            positive = 1 if score > 0 else 0
            negative = 1 if score < 0 else 0
            cursor.execute(
                "INSERT INTO tweets (text, positive, negative) VALUES (%s, %s, %s)",
                (tweet, positive, negative)
            )
        mysql.connection.commit()
        cursor.close()

        return jsonify(result), 200

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400 
    except Exception as e:
        return jsonify({"error": f"Erreur interne : {str(e)}"}), 500 
    
@tweet_blueprint.route("/", methods=["GET"])
def get_tweets():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM tweets")
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        cursor.close()

        tweets_json = {}
        for index, row in enumerate(rows, start=1):
            tweet_dict = dict(zip(columns, row))
            tweets_json[str(index)] = {
                "ID": tweet_dict.get("id"),
                "text": tweet_dict.get("text"),
                "positive": tweet_dict.get("positive"),
                "negative": tweet_dict.get("negative")
            }

        return jsonify(tweets_json), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    

@tweet_blueprint.route("/metrics", methods=["GET"])
def get_metrics():
    try:
        y_true = ['positif', 'négatif', 'positif', 'négatif', 'positif', 'positif', 'négatif']
        y_pred = ['positif', 'négatif', 'négatif', 'négatif', 'positif', 'positif', 'positif']

        metrics = calculate_metrics(y_true, y_pred)

        return jsonify(metrics), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400
