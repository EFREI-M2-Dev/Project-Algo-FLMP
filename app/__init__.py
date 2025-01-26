from flask import Flask
from app.config.db import mysql, init_db
from app.controllers.tweet_controller import tweet_blueprint

def create_app():
    app = Flask(__name__)

    init_db(app)

    app.register_blueprint(tweet_blueprint, url_prefix="/tweets")

    @app.route('/test_db')
    def test_db():
        cur = mysql.connection.cursor()
        cur.execute("SELECT 1")
        result = cur.fetchone()
        cur.close()
        
        if result:
            return "La connexion à la base de données fonctionne !"
        else:
            return "Échec de la connexion à la base de données."

    return app
