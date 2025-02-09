import os
import joblib
from app.utils.text_util import clean_text

SAVE_DIR = "models"
MODEL_NEG_PATH = os.path.join(SAVE_DIR, "model_negatif.pkl")
MODEL_POS_PATH = os.path.join(SAVE_DIR, "model_positif.pkl")
VECTORIZER_PATH = os.path.join(SAVE_DIR, "vectorizer.pkl")


def load_models():
    if not hasattr(load_models, "vectorizer"):
        if not all(os.path.exists(path) for path in [MODEL_NEG_PATH, MODEL_POS_PATH, VECTORIZER_PATH]):
            raise FileNotFoundError(f"Les fichiers suivants sont manquants : {', '.join([p for p in [MODEL_NEG_PATH, MODEL_POS_PATH, VECTORIZER_PATH] if not os.path.exists(p)])}")

        print("Chargement des modèles...")
        load_models.model_neg = joblib.load(MODEL_NEG_PATH)
        load_models.model_pos = joblib.load(MODEL_POS_PATH)
        load_models.vectorizer = joblib.load(VECTORIZER_PATH)

def analyze_text(text):
    load_models()  
    
    text_clean = clean_text(text)  
    text_vectorized = load_models.vectorizer.transform([text_clean])  

    prob_neg = load_models.model_neg.predict_proba(text_vectorized)[0][1]  
    prob_pos = load_models.model_pos.predict_proba(text_vectorized)[0][1] 

    sentiment_score = prob_pos - prob_neg

    return round(sentiment_score, 2)
