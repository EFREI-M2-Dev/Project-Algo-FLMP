import os
import joblib
from app.utils.text_util import clean_text

SAVE_DIR = "models"

model_neg = joblib.load(os.path.join(SAVE_DIR, "model_negatif.pkl"))
model_pos = joblib.load(os.path.join(SAVE_DIR, "model_positif.pkl"))
vectorizer = joblib.load(os.path.join(SAVE_DIR, "vectorizer.pkl"))

def analyze_text(text):
    text_clean = clean_text(text)  
    text_vectorized = vectorizer.transform([text_clean])  

    prob_neg = model_neg.predict_proba(text_vectorized)[0][1]  
    prob_pos = model_pos.predict_proba(text_vectorized)[0][1] 

    sentiment_score = prob_pos - prob_neg

    return round(sentiment_score, 2)