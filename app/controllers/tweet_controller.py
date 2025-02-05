from flask import Blueprint, request, jsonify
from app.models.tweet_model import TweetsRequest
from app.services.tweet_service import analyze_tweets
from app.config.db import mysql

tweet_blueprint = Blueprint("tweets", __name__)

@tweet_blueprint.route("/", methods=["POST"])
def post_tweets():
    try:
        data = request.get_json()
        tweets_request = TweetsRequest(**data)
        result = analyze_tweets(tweets_request.tweets)

        cursor = mysql.connection.cursor()
        for tweet in tweets_request.tweets:
            score = result[tweet]
            positive = 1 if score > 0 else 0
            negative = 1 if score < 0 else 0
            cursor.execute(
                "INSERT INTO tweets (text, positive, negative) VALUES (%s, %s, %s)",
                (tweet, positive, negative)
            )
        mysql.connection.commit()
        cursor.close()

        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
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