from flask import Blueprint, request, jsonify
from app.models.tweet_model import TweetsRequest
from app.services.tweet_service import analyze_tweets

tweet_blueprint = Blueprint("tweets", __name__)

@tweet_blueprint.route("/", methods=["POST"])
def post_tweets():
    try:
        data = request.get_json()

        tweets_request = TweetsRequest(**data)

        result = analyze_tweets(tweets_request.tweets)

        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
@tweet_blueprint.route("/", methods=["GET"])
def get_tweets():
    return jsonify({"message": "Hello World"}), 200
