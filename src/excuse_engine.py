"""
excuse_engine.py
----------------
Core rule-based excuse generation engine.
Loads templates from data/templates.json and fills
placeholders using NLP context from nlp_engine.py
"""

import json
import random
from datetime import datetime, timedelta
from pathlib import Path

# ── Load templates from JSON ─────────────────────────────────
BASE_DIR  = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "templates.json"

with open(DATA_PATH, "r") as f:
    TEMPLATE_DATA = json.load(f)

TEMPLATES  = {k: v for k, v in TEMPLATE_DATA.items() if k != "context_variables"}
CONTEXT    = TEMPLATE_DATA["context_variables"]


# ── Helper Utilities ─────────────────────────────────────────

def _get_new_deadline(days_ahead: int = 2) -> str:
    """Returns a deadline date string N days from today."""
    future = datetime.now() + timedelta(days=days_ahead)
    return future.strftime("%A, %d %B %Y")


def _pick_event(category: str) -> str:
    """Randomly pick a fitting event for the given category."""
    events = CONTEXT["events"].get(category, CONTEXT["events"]["emergency"])
    return random.choice(events)


def _pick_recovery(category: str) -> str:
    """Randomly pick a recovery action for the given category."""
    actions = CONTEXT["recovery_actions"].get(
        category, CONTEXT["recovery_actions"]["emergency"]
    )
    return random.choice(actions)


def _fill_template(template: str, context: dict) -> str:
    """
    Fill all {placeholders} in a template string using context dict.
    Any unfilled placeholders are cleaned up gracefully.
    """
    try:
        return template.format(**context)
    except KeyError as e:
        # If a placeholder is missing, replace it with a sensible default
        missing = str(e).strip("'")
        context[missing] = f"[{missing}]"
        return template.format(**context)


# ── Main Generation Function ─────────────────────────────────

def generate_excuse(
    situation : str,
    category  : str,
    relationship: str,
    nlp_context : dict,
    emergency : bool = False
) -> dict:
    """
    Generate a context-aware excuse.

    Args:
        situation    : Raw user input describing the situation
        category     : 'academic' | 'professional' | 'social' | 'emergency'
        relationship : 'teacher' | 'boss' | 'friend' | 'parent' | 'colleague' | 'client' | 'partner'
        nlp_context  : Output dict from nlp_engine.process_input()
        emergency    : If True, forces emergency category

    Returns:
        dict with keys: raw_excuse, category, relationship, context_used
    """

    # Emergency override
    if emergency:
        category = "emergency"

    # Resolve relationship → available key in templates
    cat_templates = TEMPLATES.get(category, TEMPLATES["academic"])

    # Find best matching relationship key, fall back to first available
    rel_key = relationship.lower()
    if rel_key not in cat_templates:
        if category == "emergency":
            rel_key = "any"
        else:
            rel_key = list(cat_templates.keys())[0]

    templates = cat_templates[rel_key]
    chosen    = random.choice(templates)

    # Build context dict for placeholder filling
    event    = _pick_event(category)
    recovery = _pick_recovery(category)
    deadline = _get_new_deadline(days_ahead=random.randint(1, 3))

    fill_context = {
        "issue"           : nlp_context.get("issue", "my failure to complete the task"),
        "event"           : event,
        "action"          : nlp_context.get("action", "fulfill my obligations"),
        "recovery_action" : recovery,
        "new_deadline"    : deadline,
        "situation"       : situation,
    }

    raw_excuse = _fill_template(chosen, fill_context)

    return {
        "raw_excuse"   : raw_excuse,
        "category"     : category,
        "relationship" : rel_key,
        "event_used"   : event,
        "deadline"     : deadline,
        "context_used" : fill_context
    }


# ── Emergency Quick Generate ─────────────────────────────────

def generate_emergency_excuse(situation: str, nlp_context: dict) -> dict:
    """One-click emergency excuse with no configuration needed."""
    return generate_excuse(
        situation    = situation,
        category     = "emergency",
        relationship = "any",
        nlp_context  = nlp_context,
        emergency    = True
    )