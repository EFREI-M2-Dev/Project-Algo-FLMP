import os
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer
from app.utils.text_util import clean_text
from app.config.db import mysql
from app import create_app

def fetch_data_from_db():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT text, positive, negative FROM tweets")
    rows = cursor.fetchall()
    cursor.close()
    return rows

  
def train():
    save_dir = "models"
    os.makedirs(save_dir, exist_ok=True)

    data = fetch_data_from_db()
    df = pd.DataFrame(data, columns=['text', 'positive', 'negative'])

    df['text_clean'] = df['text'].apply(clean_text)
    df['label'] = df.apply(lambda row: 0 if row['positive'] == 1 else 1, axis=1)
    
    create_model(df['text_clean'], df['label'])

    
def create_model(text, label):
    vectorizer = CountVectorizer(max_features=100)
    X = vectorizer.fit_transform(text)
    y = label

    X_train_neg, X_test_neg, y_train_neg, y_test_neg = train_test_split(X, y, test_size=0.25, random_state=42)
    X_train_pos, X_test_pos, y_train_pos, y_test_pos = train_test_split(X, 1 - y, test_size=0.25, random_state=42)

    model_neg = LogisticRegression()
    model_neg.fit(X_train_neg, y_train_neg)

    model_pos = LogisticRegression()
    model_pos.fit(X_train_pos, y_train_pos)

    joblib.dump(model_neg, os.path.join(save_dir, "model_negatif.pkl"))
    joblib.dump(model_pos, os.path.join(save_dir, "model_positif.pkl"))
    joblib.dump(vectorizer, os.path.join(save_dir, "vectorizer.pkl"))


def main():
    app = create_app()
    with app.app_context():
        train()

if __name__ == "__main__":
    main()
