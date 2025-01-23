from fastapi import APIRouter
from app.models.tweet_model import TweetsRequest
from app.services.tweet_service import analyze_tweets

router = APIRouter()

@router.post("/")
def post_tweets(payload: TweetsRequest):
    return analyze_tweets(payload.tweets)