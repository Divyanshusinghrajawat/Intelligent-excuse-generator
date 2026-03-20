"""
nlp_engine.py
-------------
NLP processing using spaCy (local) with NLTK fallback (cloud).
Automatically detects which library is available.
"""

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download('vader_lexicon', quiet=True)
nltk.download('punkt',         quiet=True)
nltk.download('punkt_tab',     quiet=True)
nltk.download('stopwords',     quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)

# ── Try spaCy, fall back to NLTK only ────────────────────────
try:
    import spacy
    nlp = spacy.load("en_core_web_sm")
    USE_SPACY = True
except Exception:
    USE_SPACY = False

sid       = SentimentIntensityAnalyzer()
STOP_WORDS = set(stopwords.words('english'))

URGENCY_WORDS = {
    "urgent", "emergency", "immediately", "asap", "critical",
    "deadline", "now", "today", "tonight", "last minute",
    "right now", "hurry", "quick"
}


def extract_keywords(text: str) -> dict:
    keywords = {
        "entities"  : [],
        "nouns"     : [],
        "verbs"     : [],
        "adjectives": [],
        "urgency"   : False
    }

    words = word_tokenize(text.lower())

    # Check urgency
    for w in words:
        if w in URGENCY_WORDS:
            keywords["urgency"] = True

    if USE_SPACY:
        doc = nlp(text.lower())
        for ent in doc.ents:
            if ent.label_ in ("PERSON", "ORG", "GPE", "EVENT", "DATE", "TIME"):
                keywords["entities"].append(ent.text)
        for token in doc:
            if token.is_stop or token.is_punct or len(token.text) < 3:
                continue
            if token.pos_ == "NOUN" and token.lemma_ not in STOP_WORDS:
                keywords["nouns"].append(token.lemma_)
            elif token.pos_ == "VERB" and token.lemma_ not in STOP_WORDS:
                keywords["verbs"].append(token.lemma_)
            elif token.pos_ == "ADJ":
                keywords["adjectives"].append(token.lemma_)
    else:
        # NLTK fallback — POS tagging
        tagged = nltk.pos_tag(words)
        for word, tag in tagged:
            if word in STOP_WORDS or len(word) < 3:
                continue
            if tag.startswith("NN"):
                keywords["nouns"].append(word)
            elif tag.startswith("VB"):
                keywords["verbs"].append(word)
            elif tag.startswith("JJ"):
                keywords["adjectives"].append(word)

    # Deduplicate
    for k in ["entities", "nouns", "verbs", "adjectives"]:
        keywords[k] = list(dict.fromkeys(keywords[k]))[:5]

    return keywords


def analyze_sentiment(text: str) -> str:
    scores = sid.polarity_scores(text)
    if scores['compound'] >= 0.05:
        return "positive"
    elif scores['compound'] <= -0.05:
        return "negative"
    return "neutral"


def infer_action(text: str, category: str) -> str:
    action_hints = {
        "academic"     : ["submit", "attend", "complete", "finish", "write", "present"],
        "professional" : ["deliver", "attend", "complete", "send", "submit", "join"],
        "social"       : ["attend", "come", "join", "meet", "arrive", "show"],
        "emergency"    : ["respond", "attend", "communicate", "reach"]
    }
    hints  = action_hints.get(category, action_hints["professional"])
    words  = word_tokenize(text.lower())
    tagged = nltk.pos_tag(words)

    for word, tag in tagged:
        if word in hints:
            return f"{word} as required"

    return "fulfill my obligations"


def infer_issue(text: str, category: str) -> str:
    issue_map = {
        "academic"     : "my inability to submit the work on time",
        "professional" : "the delay in delivering the expected output",
        "social"       : "my absence from our plans",
        "emergency"    : "my sudden unavailability"
    }
    words = word_tokenize(text[:120].lower())
    tagged = nltk.pos_tag(words)
    nouns = [w for w, t in tagged if t.startswith("NN")
             and w not in STOP_WORDS and len(w) > 3]
    if nouns:
        return f"my failure to address {nouns[0]} on time"
    return issue_map.get(category, issue_map["professional"])


def process_input(text: str, category: str) -> dict:
    keywords  = extract_keywords(text)
    sentiment = analyze_sentiment(text)
    action    = infer_action(text, category)
    issue     = infer_issue(text, category)

    return {
        "keywords"  : keywords,
        "sentiment" : sentiment,
        "action"    : action,
        "issue"     : issue,
        "is_urgent" : keywords["urgency"]
    }