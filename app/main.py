from fastapi import FastAPI
from app.controllers.tweet_controller import router as tweet_router

app = FastAPI()

app.include_router(tweet_router, prefix="/tweets", tags=["Tweets"])
