"""
formatter.py
------------
Formats the raw excuse into three output styles:
  - plain     : simple paragraph text
  - letter    : formal letter format
  - whatsapp  : casual messaging format
"""

from datetime import datetime


# ── Sender placeholder (can be overridden) ───────────────────
DEFAULT_SENDER = "Divyanshu"


def _today() -> str:
    return datetime.now().strftime("%d %B %Y")


def _greeting(relationship: str, tone: str) -> str:
    """Generate appropriate greeting based on relationship and tone."""
    formal = {
        "teacher"   : "Respected Sir/Ma'am,",
        "boss"      : "Dear Sir/Ma'am,",
        "client"    : "Dear Sir/Ma'am,",
        "parent"    : "Dear Maa/Papa,",
        "colleague" : "Hi,",
        "friend"    : "Hey,",
        "partner"   : "Hey,",
        "any"       : "To Whom It May Concern,"
    }
    casual = {
        "teacher"   : "Hi Sir/Ma'am,",
        "boss"      : "Hi,",
        "client"    : "Dear Sir/Ma'am,",
        "parent"    : "Maa/Papa,",
        "colleague" : "Hey,",
        "friend"    : "Yaar,",
        "partner"   : "Hey love,",
        "any"       : "Hi,"
    }
    pool = formal if tone == "formal" else casual
    return pool.get(relationship, pool.get("any", "Dear,"))


def _closing(relationship: str, tone: str) -> str:
    """Generate appropriate closing line."""
    formal_closings = [
        "I sincerely apologize for the inconvenience caused and assure you of my commitment going forward.",
        "I appreciate your understanding and patience in this matter.",
        "Thank you for your consideration. I remain fully committed to my responsibilities."
    ]
    casual_closings = [
        "Really sorry again, will make sure this doesn't happen!",
        "Thanks for understanding, means a lot.",
        "Sorry once more — I'll sort this out soon!"
    ]
    import random
    if tone == "formal":
        return random.choice(formal_closings)
    return random.choice(casual_closings)


# ── Format Functions ─────────────────────────────────────────

def format_plain(excuse: str, relationship: str, tone: str) -> str:
    """
    Plain paragraph format — clean text, no decoration.
    """
    greeting = _greeting(relationship, tone)
    closing  = _closing(relationship, tone)
    return f"{greeting}\n\n{excuse}\n\n{closing}\n\n{DEFAULT_SENDER}"


def format_letter(
    excuse      : str,
    relationship: str,
    sender_name : str = DEFAULT_SENDER,
    subject     : str = "Explanation for Absence / Delay"
) -> str:
    """
    Formal letter format with date, subject, greeting, body, closing.
    """
    recipient_map = {
        "teacher"   : "The Class Teacher / Professor",
        "boss"      : "The Manager / Supervisor",
        "client"    : "The Concerned Client",
        "parent"    : "Parents/Guardian",
        "colleague" : "The Concerned Colleague",
        "friend"    : "Friend",
        "partner"   : "Partner",
        "any"       : "The Concerned Authority"
    }
    recipient = recipient_map.get(relationship, "The Concerned Authority")

    letter = f"""
{'='*55}
                    FORMAL LETTER
{'='*55}
Date    : {_today()}
To      : {recipient}
Subject : {subject}
{'─'*55}

Respected Sir/Ma'am,

{excuse}

I sincerely apologize for any inconvenience caused and
assure you that I take my responsibilities seriously.
I remain committed to ensuring this does not recur.

Thanking you for your understanding and consideration.

Yours sincerely,
{sender_name}
{'='*55}
""".strip()

    return letter


def format_whatsapp(excuse: str, relationship: str) -> str:
    """
    WhatsApp-style casual message format.
    Short, conversational, with emoji.
    """
    casual_openers = {
        "teacher"   : "Sir/Ma'am really sorry to message like this 🙏",
        "boss"      : "Hi, really sorry for the short notice 🙏",
        "parent"    : "Maa/Papa I'm really sorry 😔",
        "colleague" : "Hey, really sorry about this 😅",
        "friend"    : "Yaar I'm so sorry 😭",
        "partner"   : "Hey I'm really sorry 😔",
        "client"    : "Hi, sincere apologies for this 🙏",
        "any"       : "Hi, sorry for the inconvenience 🙏"
    }

    opener  = casual_openers.get(relationship, casual_openers["any"])
    # Keep whatsapp version concise — first 2 sentences only
    sentences = excuse.replace("\n", " ").split(". ")
    short     = ". ".join(sentences[:2]).strip()
    if not short.endswith("."):
        short += "."

    return f"{opener}\n\n{short}\n\nWill update you soon 🙏"


# ── Master Formatter ─────────────────────────────────────────

def format_all(
    excuse      : str,
    relationship: str,
    tone        : str = "formal",
    sender_name : str = DEFAULT_SENDER
) -> dict:
    """
    Generate all three formats at once.

    Returns:
        dict with keys: plain, letter, whatsapp
    """
    return {
        "plain"    : format_plain(excuse, relationship, tone),
        "letter"   : format_letter(excuse, relationship, sender_name),
        "whatsapp" : format_whatsapp(excuse, relationship)
    }