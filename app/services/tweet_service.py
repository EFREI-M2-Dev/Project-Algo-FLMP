from app.config.db import mysql
from app.services.predict_service import analyze_text

def analyze_tweets(tweets: list[str]) -> dict:
    response = {}
    for tweet in tweets:
        score = analyze_text(tweet)
        response[tweet] = score

    cursor = mysql.connection.cursor()
    for tweet in tweets:
        score = response.get(tweet, 0)
        positive = 1 if score > 0 else 0
        negative = 1 if score < 0 else 0
        cursor.execute(
            "INSERT INTO tweets (text, positive, negative) VALUES (%s, %s, %s)",
            (tweet, positive, negative)
        )
    mysql.connection.commit()
    cursor.close()
    
    return response


def fetch_tweets():
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
    
    return tweets_json
