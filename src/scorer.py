"""
scorer.py
---------
Believability scoring using a scikit-learn ML pipeline.
Trained on synthetic excuse data from data/training_data.json.
Scores excuses on a scale of 1-10 with feedback tips.
"""

import json
import pickle
import numpy as np
from pathlib import Path

from sklearn.pipeline         import Pipeline
from sklearn.linear_model     import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection  import train_test_split
from sklearn.metrics          import accuracy_score

# ── Paths ────────────────────────────────────────────────────
BASE_DIR      = Path(__file__).resolve().parent.parent
DATA_PATH     = BASE_DIR / "data"  / "training_data.json"
MODEL_PATH    = BASE_DIR / "models" / "scorer_model.pkl"

# ── Score bands ──────────────────────────────────────────────
SCORE_BANDS = {
    2: (8, 10),   # high believability
    1: (5,  7),   # medium
    0: (1,  4),   # low
}

FEEDBACK_TIPS = {
    2: [
        "Strong excuse — specific and verifiable details make it highly credible.",
        "Excellent believability. The context is realistic and hard to dispute.",
        "Very convincing. Mentioning documentation would make it bulletproof."
    ],
    1: [
        "Decent excuse but adding a specific detail (date, place) would strengthen it.",
        "Moderately believable. Try referencing a verifiable event for more impact.",
        "Could be more convincing — include a concrete reason with supporting context."
    ],
    0: [
        "Low believability. The excuse sounds vague — add specific circumstances.",
        "Needs work. Generic excuses are easy to see through. Be more specific.",
        "Weak excuse. Mention a concrete event with time and context to improve."
    ]
}


# ── Model Training ───────────────────────────────────────────

def train_model(save: bool = True) -> Pipeline:
    """
    Train the believability classifier on training_data.json.
    Saves model to models/scorer_model.pkl if save=True.
    """
    with open(DATA_PATH, "r") as f:
        raw = json.load(f)

    texts  = [item[0] for item in raw["data"]]
    labels = [item[1] for item in raw["data"]]

    X_train, X_test, y_train, y_test = train_test_split(
        texts, labels, test_size=0.2, random_state=42, stratify=labels
    )

    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(
            ngram_range = (1, 2),
            max_features = 5000,
            stop_words   = "english"
        )),
        ("clf", LogisticRegression(
            max_iter = 1000,
            C        = 1.0,
            solver   = "lbfgs"
        ))
    ])

    pipeline.fit(X_train, y_train)

    # Evaluate
    y_pred    = pipeline.predict(X_test)
    accuracy  = accuracy_score(y_test, y_pred)
    print(f"   Model trained — Accuracy: {accuracy * 100:.1f}%")

    if save:
        MODEL_PATH.parent.mkdir(exist_ok=True)
        with open(MODEL_PATH, "wb") as f:
            pickle.dump(pipeline, f)
        print(f"   Model saved to {MODEL_PATH}")

    return pipeline


def load_model() -> Pipeline:
    """Load saved model, or train a fresh one if not found."""
    if MODEL_PATH.exists():
        with open(MODEL_PATH, "rb") as f:
            return pickle.load(f)
    print("   No saved model found — training now...")
    return train_model(save=True)


# ── Scoring ──────────────────────────────────────────────────

def score_excuse(excuse_text: str, model: Pipeline = None) -> dict:
    """
    Score an excuse for believability.

    Returns:
        dict with keys: score (1-10), label, feedback, confidence
    """
    if model is None:
        model = load_model()

    # Predict class and probability
    pred_class   = model.predict([excuse_text])[0]
    probabilities = model.predict_proba([excuse_text])[0]
    confidence   = round(float(np.max(probabilities)) * 100, 1)

    # Map class to numeric score in range
    low, high  = SCORE_BANDS[pred_class]
    base_score = (low + high) // 2

    # Fine-tune score using confidence
    if confidence > 80:
        score = high
    elif confidence > 60:
        score = base_score
    else:
        score = low

    # Label
    label_map = {2: "High", 1: "Medium", 0: "Low"}
    label     = label_map[pred_class]

    # Feedback tip
    import random
    feedback = random.choice(FEEDBACK_TIPS[pred_class])

    return {
        "score"      : score,
        "label"      : label,
        "feedback"   : feedback,
        "confidence" : confidence,
        "class"      : pred_class
    }


# ── Train on first import if model missing ───────────────────
_model_cache = None

def get_model() -> Pipeline:
    """Cached model loader — trains once per session."""
    global _model_cache
    if _model_cache is None:
        _model_cache = load_model()
    return _model_cache