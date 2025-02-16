import pandas as pd
from app.config.db import mysql
from app.services.train_service import create_model


def push_new_datas(tweets):
    cursor = mysql.connection.cursor()

    for tweet in tweets:
        text, label = tweet["text"], tweet["label"]
        positive = 1 if label == 0 else 0
        negative = 1 if label == 1 else 0
        cursor.execute(
            "INSERT INTO tweets (text, positive, negative) VALUES (%s, %s, %s)",
            (text, positive, negative)
        )

    mysql.connection.commit()
    cursor.close()
    reinforcement()

def reinforcement():
    from app import create_app

    app = create_app()
    with app.app_context():
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT text, negative FROM tweets")
        rows = cursor.fetchall()
        cursor.close()

        if not rows:
            print("⚠️ Aucune donnée dans la base pour entraîner le modèle.")
            return

        # Extraction des textes et labels
        texts = [row[0] for row in rows]
        labels = [row[1] for row in rows]  # negative = 1, sinon 0

        create_model(texts, pd.Series(labels))

if __name__ == "__main__":
    reinforcement()