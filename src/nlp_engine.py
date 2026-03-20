"""
nlp_engine.py
-------------
NLP processing using NLTK only (cloud compatible).
"""

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download('vader_lexicon',              quiet=True)
nltk.download('punkt',                      quiet=True)
nltk.download('punkt_tab',                  quiet=True)
nltk.download('stopwords',                  quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)
nltk.download('averaged_perceptron_tagger_eng', quiet=True)

sid        = SentimentIntensityAnalyzer()
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

    words  = word_tokenize(text.lower())
    tagged = nltk.pos_tag(words)

    for word, tag in tagged:
        if word in URGENCY_WORDS:
            keywords["urgency"] = True
        if word in STOP_WORDS or len(word) < 3:
            continue
        if tag.startswith("NN"):
            keywords["nouns"].append(word)
        elif tag.startswith("VB"):
            keywords["verbs"].append(word)
        elif tag.startswith("JJ"):
            keywords["adjectives"].append(word)

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
    words  = word_tokenize(text[:120].lower())
    tagged = nltk.pos_tag(words)
    nouns  = [w for w, t in tagged
              if t.startswith("NN") and w not in STOP_WORDS and len(w) > 3]
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