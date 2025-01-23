import random

def analyze_tweets(tweets: list[str]) -> dict:
    response = {}
    for tweet in tweets:
        # Mocking the score
        score = random.randint(-1, 1)
        response[tweet] = score
    return response