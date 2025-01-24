from flask import Flask
from app.controllers.tweet_controller import tweet_blueprint

app = Flask(__name__)

app.register_blueprint(tweet_blueprint, url_prefix="/tweets")

if __name__ == "__main__":
    app.run(debug=True)
