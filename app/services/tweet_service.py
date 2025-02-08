from app.services.predict_service import analyze_text

def analyze_tweets(tweets: list[str]) -> dict:
    response = {}
    for tweet in tweets:
        score = analyze_text(tweet)
        response[tweet] = score
    return response