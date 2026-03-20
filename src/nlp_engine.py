"""
nlp_engine.py
-------------
Handles all NLP processing using spaCy and NLTK.
- Keyword extraction
- Intent/urgency detection
- Sentiment analysis
- Context inference
"""

import spacy
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords

# Download required NLTK data
nltk.download('vader_lexicon', quiet=True)
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

# Load spaCy model
nlp = spacy.load("en_core_web_sm")
sid = SentimentIntensityAnalyzer()
STOP_WORDS = set(stopwords.words('english'))

URGENCY_WORDS = {
    "urgent", "emergency", "immediately", "asap", "critical",
    "deadline", "now", "today", "tonight", "last minute",
    "right now", "as soon as possible", "hurry", "quick"
}


def extract_keywords(text: str) -> dict:
    """
    Extract meaningful keywords from user situation text using spaCy.

    Returns:
        dict with keys: entities, nouns, verbs, adjectives, urgency
    """
    doc = nlp(text.lower())

    keywords = {
        "entities"   : [],
        "nouns"      : [],
        "verbs"      : [],
        "adjectives" : [],
        "urgency"    : False
    }

    # Named entity extraction
    for ent in doc.ents:
        if ent.label_ in ("PERSON", "ORG", "GPE", "EVENT", "DATE", "TIME"):
            keywords["entities"].append(ent.text)

    # POS-based extraction
    for token in doc:
        if token.is_stop or token.is_punct or len(token.text) < 3:
            continue
        if token.pos_ == "NOUN" and token.lemma_ not in STOP_WORDS:
            keywords["nouns"].append(token.lemma_)
        elif token.pos_ == "VERB" and token.lemma_ not in STOP_WORDS:
            keywords["verbs"].append(token.lemma_)
        elif token.pos_ == "ADJ":
            keywords["adjectives"].append(token.lemma_)
        if token.text in URGENCY_WORDS:
            keywords["urgency"] = True

    # Deduplicate and limit
    for k in ["entities", "nouns", "verbs", "adjectives"]:
        keywords[k] = list(dict.fromkeys(keywords[k]))[:5]

    return keywords


def analyze_sentiment(text: str) -> str:
    """
    Returns 'positive', 'negative', or 'neutral' based on VADER sentiment.
    Used to adjust excuse tone.
    """
    scores = sid.polarity_scores(text)
    if scores['compound'] >= 0.05:
        return "positive"
    elif scores['compound'] <= -0.05:
        return "negative"
    return "neutral"


def infer_action(text: str, category: str) -> str:
    """
    Infer the specific action that was missed from user input.
    e.g. 'submit the assignment', 'attend the meeting'
    """
    doc = nlp(text.lower())

    action_hints = {
        "academic"     : ["submit", "attend", "complete", "finish", "write", "present"],
        "professional" : ["deliver", "attend", "complete", "send", "submit", "join"],
        "social"       : ["attend", "come", "join", "meet", "arrive", "show"],
        "emergency"    : ["respond", "attend", "communicate", "reach"]
    }

    hints = action_hints.get(category, action_hints["professional"])

    for token in doc:
        if token.lemma_ in hints:
            for child in token.children:
                if child.dep_ in ("dobj", "pobj"):
                    return f"{token.lemma_} the {child.text}"
            return f"{token.lemma_} as required"

    return "fulfill my obligations"


def infer_issue(text: str, category: str) -> str:
    """
    Generate a brief issue phrase from the situation text.
    """
    issue_map = {
        "academic"     : "my inability to submit the work on time",
        "professional" : "the delay in delivering the expected output",
        "social"       : "my absence from our plans",
        "emergency"    : "my sudden unavailability"
    }

    doc = nlp(text[:120])
    nouns = [t.text for t in doc if t.pos_ == "NOUN" and not t.is_stop]
    if nouns:
        return f"my failure to address {nouns[0]} on time"

    return issue_map.get(category, issue_map["professional"])


def process_input(text: str, category: str) -> dict:
    """
    Master function — runs full NLP pipeline on user input.
    Returns a context dict used by the excuse engine.
    """
    keywords = extract_keywords(text)
    sentiment = analyze_sentiment(text)
    action = infer_action(text, category)
    issue = infer_issue(text, category)

    return {
        "keywords"  : keywords,
        "sentiment" : sentiment,
        "action"    : action,
        "issue"     : issue,
        "is_urgent" : keywords["urgency"]
    }