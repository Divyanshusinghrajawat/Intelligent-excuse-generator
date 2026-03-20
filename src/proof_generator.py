"""
proof_generator.py
------------------
Generates contextual proof and evidence suggestions
based on excuse category, event type and relationship.
"""

from pathlib import Path


# ── Proof Suggestion Bank ────────────────────────────────────

PROOF_BANK = {
    "academic": {
        "medical": [
            "📄 Medical certificate from a registered doctor (obtain within 3 days of visit)",
            "🏥 Hospital/clinic OPD receipt or discharge summary",
            "📱 Appointment confirmation SMS or email from the hospital",
            "💊 Prescription slip with date matching the absence",
            "📝 Written note from parent/guardian confirming the situation"
        ],
        "technical": [
            "🖥️  Screenshot of internet outage complaint or ISP ticket number",
            "📸 Photo of error message or non-functional device",
            "🔌 Power outage complaint reference number from electricity board",
            "📧 Email to IT support sent around the time of the issue",
            "📱 Screenshot showing no connectivity (airplane mode timestamp)"
        ],
        "family": [
            "📝 Written note from parent or guardian on letterhead",
            "🏥 Hospital admission slip if family member was hospitalized",
            "✈️  Travel ticket showing emergency outstation travel",
            "📞 Offer to have parent/guardian speak with the teacher directly",
            "📄 Death certificate or funeral notice in case of bereavement"
        ],
        "general": [
            "📝 Written application explaining the circumstances clearly",
            "👨‍👩‍👧 Parent/guardian written confirmation of the situation",
            "📱 Any timestamp-based evidence (messages, emails, receipts)",
            "🗓️  Show calendar/planner entries around the date in question",
            "📧 Any email correspondence from that time period"
        ]
    },
    "professional": {
        "medical": [
            "📄 Medical certificate from a registered practitioner",
            "🏥 Hospital discharge summary or OPD receipt",
            "💊 Prescription with date matching the absence period",
            "📧 Email to HR informing them of the medical situation",
            "📱 Telemedicine consultation screenshot if applicable"
        ],
        "technical": [
            "📧 Forward the incident/outage alert email to your manager",
            "📊 Incident report or system downtime log",
            "🖥️  Screenshot of error messages or monitoring alerts",
            "📱 IT helpdesk ticket number and timestamp",
            "📋 Brief written incident timeline document"
        ],
        "travel": [
            "🎫 Flight/train cancellation or delay confirmation",
            "📧 Booking reference email showing travel disruption",
            "🚗 Cab/transport receipt showing travel time",
            "🗺️  Traffic or weather alert screenshot for that day",
            "📱 Google Maps timeline screenshot if available"
        ],
        "general": [
            "📧 Email sent to relevant stakeholders at the time",
            "📊 Updated status report showing current progress",
            "📅 Revised timeline document with new delivery dates",
            "💬 Slack/Teams message history showing the situation",
            "📋 Brief written explanation on company letterhead"
        ]
    },
    "social": {
        "general": [
            "📱 Message sent at the time explaining the situation",
            "🏥 Medical receipt if health-related",
            "📞 Offer to call and explain in detail",
            "📸 Photo evidence if relevant and appropriate",
            "🗓️  Show the conflicting commitment on your calendar"
        ]
    },
    "emergency": {
        "general": [
            "📱 Send a follow-up message once the emergency is resolved",
            "🏥 Medical or emergency documentation if applicable",
            "👨‍👩‍👧 Word from a family member if verification is needed",
            "📄 Any official document related to the emergency",
            "📞 Offer a direct call to explain once situation stabilizes"
        ]
    }
}


# ── Event Type Detector ──────────────────────────────────────

def _detect_event_type(event_text: str) -> str:
    """Classify the event into a proof category."""
    event_lower = event_text.lower()

    medical_keywords  = {"medical", "hospital", "sick", "illness", "health",
                         "doctor", "emergency", "migraine", "fever", "injury",
                         "accident", "allergic", "bereavement", "death", "funeral"}
    technical_keywords = {"internet", "power", "outage", "server", "system",
                          "crash", "connectivity", "electricity", "laptop", "device"}
    travel_keywords    = {"travel", "traffic", "flight", "train", "transport",
                          "vehicle", "breakdown", "stuck", "commute"}
    family_keywords    = {"family", "parent", "mother", "father", "brother",
                          "sister", "relative", "home", "guardian"}

    words = set(event_lower.split())

    if words & medical_keywords:
        return "medical"
    if words & technical_keywords:
        return "technical"
    if words & travel_keywords:
        return "travel"
    if words & family_keywords:
        return "family"
    return "general"


# ── Main Function ────────────────────────────────────────────

def get_proof_suggestions(
    category   : str,
    event_text : str,
    count      : int = 3
) -> dict:
    """
    Get proof/evidence suggestions based on category and event.

    Args:
        category   : 'academic' | 'professional' | 'social' | 'emergency'
        event_text : The event string used in the excuse
        count      : Number of suggestions to return

    Returns:
        dict with keys: event_type, suggestions, disclaimer
    """
    event_type = _detect_event_type(event_text)

    # Get category bank
    cat_bank = PROOF_BANK.get(category, PROOF_BANK["emergency"])

    # Get event-specific suggestions, fall back to general
    suggestions = cat_bank.get(event_type, cat_bank.get("general", []))

    # Limit count
    suggestions = suggestions[:count]

    disclaimer = (
        "⚠️  These are suggestions only. Always provide genuine "
        "documentation. Fabricating proof is unethical and can have "
        "serious consequences."
    )

    return {
        "event_type"  : event_type,
        "suggestions" : suggestions,
        "disclaimer"  : disclaimer
    }