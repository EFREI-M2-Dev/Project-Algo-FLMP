import os
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer
from app.utils.text_util import clean_text

save_dir = "models"
os.makedirs(save_dir, exist_ok=True)

csv_file = "app/assets/tweets_data.csv"
df = pd.read_csv(csv_file)

df['text_clean'] = df['text'].apply(clean_text)

vectorizer = CountVectorizer(max_features=100)
X = vectorizer.fit_transform(df['text_clean'])
y = df['label']

X_train_neg, X_test_neg, y_train_neg, y_test_neg = train_test_split(X, y, test_size=0.25, random_state=42)
X_train_pos, X_test_pos, y_train_pos, y_test_pos = train_test_split(X, 1 - y, test_size=0.25, random_state=42)

model_neg = LogisticRegression()
model_neg.fit(X_train_neg, y_train_neg)

model_pos = LogisticRegression()
model_pos.fit(X_train_pos, y_train_pos)

joblib.dump(model_neg, os.path.join(save_dir, "model_negatif.pkl"))
joblib.dump(model_pos, os.path.join(save_dir, "model_positif.pkl"))
joblib.dump(vectorizer, os.path.join(save_dir, "vectorizer.pkl"))
