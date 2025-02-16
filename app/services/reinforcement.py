import os
import joblib
import pandas as pd
from app.config.db import mysql
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer


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

def reinforcement():
    save_dir = "models"

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

        vectorizer = CountVectorizer(max_features=100)
        X = vectorizer.fit_transform(texts)
        y = pd.Series(labels)

        X_train_neg, X_test_neg, y_train_neg, y_test_neg = train_test_split(X, y, test_size=0.25, random_state=42)
        X_train_pos, X_test_pos, y_train_pos, y_test_pos = train_test_split(X, 1 - y, test_size=0.25, random_state=42)

        model_neg = LogisticRegression()
        model_neg.fit(X_train_neg, y_train_neg)

        model_pos = LogisticRegression()
        model_pos.fit(X_train_pos, y_train_pos)

        joblib.dump(model_neg, os.path.join(save_dir, "model_negatif.pkl"))
        joblib.dump(model_pos, os.path.join(save_dir, "model_positif.pkl"))
        joblib.dump(vectorizer, os.path.join(save_dir, "vectorizer.pkl"))

if __name__ == "__main__":
    reinforcement()