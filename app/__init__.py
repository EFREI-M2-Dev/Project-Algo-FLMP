from flask import Flask
from app.config.db import mysql, init_db
from app.controllers.tweet_controller import tweet_blueprint

def create_app():
    app = Flask(__name__)

    init_db(app)

    app.register_blueprint(tweet_blueprint, url_prefix="/tweets")

    return app
