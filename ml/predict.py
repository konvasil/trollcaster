# ml/predict.py
import joblib
from pathlib import Path

ml_path = Path(__file__).parent
model = joblib.load(ml_path / "model.pkl")
vectorizer = joblib.load(ml_path / "vectorizer.pkl")

def is_troll(message: str) -> bool:
    x = vectorizer.transform([message])
    return bool(model.predict(x)[0])