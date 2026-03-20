"""
app.py
------
Streamlit web interface for the Intelligent Excuse Generator.
Run with: streamlit run app.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
from src.nlp_engine      import process_input
from src.excuse_engine   import generate_excuse, generate_emergency_excuse
from src.scorer          import get_model, score_excuse
from src.formatter       import format_all
from src.proof_generator import get_proof_suggestions

# ── Page Config ───────────────────────────────────────────────
st.set_page_config(
    page_title = "Intelligent Excuse Generator",
    page_icon  = "🎭",
    layout     = "centered"
)

# ── Load ML Model (cached) ────────────────────────────────────
@st.cache_resource
def load_model():
    return get_model()

MODEL = load_model()

# ── Prebuilt Situations ───────────────────────────────────────
PREBUILT = {
    "academic": {
        "-- Select a prebuilt situation --"             : "",
        "Missed assignment deadline (medical)"          : "I missed the assignment deadline because I was hospitalized due to a sudden medical emergency.",
        "Absent from class (family emergency)"          : "I could not attend class today due to an urgent family emergency that required my immediate presence.",
        "Late submission (power outage)"                : "I was unable to submit my work on time due to a power outage that lasted the entire night.",
        "Missed exam (severe illness)"                  : "I could not appear for the examination as I was suffering from severe fever and was advised bed rest.",
        "Missed presentation (internet issue)"          : "I could not join the online presentation due to a complete internet connectivity failure in my area.",
    },
    "professional": {
        "-- Select a prebuilt situation --"             : "",
        "Late to work (traffic)"                        : "I was late to the office today due to an unexpected traffic jam caused by an accident on the main road.",
        "Missed meeting (health issue)"                 : "I was unable to attend the scheduled meeting due to a sudden health issue requiring immediate medical attention.",
        "Delayed delivery (technical failure)"          : "The project delivery got delayed due to a critical server outage that affected our entire development environment.",
        "Absent from office (family crisis)"            : "I had to take an unplanned leave today as there was an urgent family health crisis that needed my presence.",
        "Missed deadline (system crash)"                : "I could not meet the deadline as my system crashed and I lost significant progress on the work.",
    },
    "social": {
        "-- Select a prebuilt situation --"             : "",
        "Missed friend's event (work emergency)"        : "I could not attend your event because there was a last minute work emergency I had to handle urgently.",
        "Late to meetup (vehicle breakdown)"            : "I was late because my vehicle broke down on the way and I had to wait for roadside assistance.",
        "Cancelled plans (sudden illness)"              : "I had to cancel our plans as I suddenly fell ill and was not in a condition to step out.",
    },
    "emergency": {
        "-- Select a prebuilt situation --"             : "",
        "General emergency"                             : "I am currently dealing with an urgent emergency and am unable to fulfil my commitments at this time.",
        "Medical emergency"                             : "I am facing a medical emergency involving a family member and need to be at the hospital immediately.",
        "Accident situation"                            : "I have been involved in a minor accident and am currently dealing with the necessary procedures.",
    }
}

# ── Header ────────────────────────────────────────────────────
st.title("🎭 Intelligent Excuse Generator")
st.markdown(
    "AI-powered · NLP-driven · Context-aware · Fully offline  \n"
    "Generate realistic excuses for academic, professional, social and emergency situations."
)
st.divider()

# ── Sidebar ───────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Configuration")

    category = st.selectbox(
        "Category",
        ["academic", "professional", "social", "emergency"],
        format_func=str.capitalize
    )

    relationship = st.selectbox(
        "Recipient",
        ["teacher", "boss", "parent", "friend", "colleague", "client", "partner"],
        format_func=str.capitalize
    )

    tone = st.selectbox(
        "Tone",
        ["formal", "casual"],
        format_func=str.capitalize
    )

    output_format = st.radio(
        "Output Format",
        ["Plain", "Formal Letter", "WhatsApp"],
        horizontal=True
    )

    proof_count = st.slider("Proof suggestions", 1, 5, 3)

    st.divider()
    st.markdown("**About**")
    st.caption(
        "Built with Python · spaCy · NLTK · "
        "scikit-learn · Streamlit  \n"
        "Internship Capstone Project"
    )

# ── Quick Fill ────────────────────────────────────────────────
st.subheader("⚡ Quick Fill")
quick_options = list(PREBUILT[category].keys())
selected_quick = st.selectbox("Select a prebuilt situation", quick_options)

# ── Situation Input ───────────────────────────────────────────
st.subheader("📝 Your Situation")

default_text = PREBUILT[category].get(selected_quick, "")
situation = st.text_area(
    "Describe your situation (or edit the quick fill above):",
    value    = default_text,
    height   = 100,
    placeholder = "e.g. I missed the assignment deadline because of a power cut..."
)

# ── Buttons ───────────────────────────────────────────────────
col1, col2 = st.columns(2)
generate_clicked  = col1.button("✨ Generate Excuse",  type="primary",    use_container_width=True)
emergency_clicked = col2.button("🚨 Emergency Mode",   type="secondary",  use_container_width=True)

# ── Generation Logic ──────────────────────────────────────────
def run_generation(situation_text, is_emergency=False):
    if not situation_text.strip():
        situation_text = "I have an urgent emergency and cannot fulfil my obligations."

    with st.spinner("Generating excuse..."):
        ctx = process_input(situation_text, "emergency" if is_emergency else category)

        if is_emergency:
            result = generate_emergency_excuse(situation_text, ctx)
        else:
            result = generate_excuse(
                situation    = situation_text,
                category     = category,
                relationship = relationship,
                nlp_context  = ctx
            )

        raw_excuse   = result["raw_excuse"]
        event        = result["event_used"]
        cat          = result["category"]

        # Format
        fmt_map  = {"Plain": "plain", "Formal Letter": "letter", "WhatsApp": "whatsapp"}
        formats  = format_all(raw_excuse, result["relationship"], tone)
        formatted = formats[fmt_map[output_format]]

        # Score
        score = score_excuse(raw_excuse, MODEL)

        # Proof
        proof = get_proof_suggestions(cat, event, count=proof_count)

    # ── Output ────────────────────────────────────────────────
    st.divider()

    tag = "🚨 EMERGENCY" if is_emergency else f"📂 {cat.upper()}"
    st.subheader(f"🎭 Generated Excuse  `{tag}`")

    st.text_area(
        label      = "Your excuse (copy from here):",
        value      = formatted,
        height     = 220,
        key        = "output_box"
    )

    # Score
    st.subheader("📊 Believability Score")
    score_color = {"High": "green", "Medium": "orange", "Low": "red"}
    col_a, col_b = st.columns([1, 3])
    col_a.metric("Score", f"{score['score']} / 10", delta=score["label"])
    col_b.info(f"💡 {score['feedback']}")

    # Score bar
    st.progress(score["score"] / 10)

    # Proof
    st.subheader("🗂️ Proof Suggestions")
    st.caption(f"Event detected: `{event}`")
    for suggestion in proof["suggestions"]:
        st.markdown(f"- {suggestion}")
    st.warning(proof["disclaimer"])

    # NLP insights
    with st.expander("🔬 NLP Analysis (what the engine extracted)"):
        st.json({
            "keywords_extracted" : ctx["keywords"]["nouns"],
            "action_inferred"    : ctx["action"],
            "urgency_detected"   : ctx["is_urgent"],
            "sentiment"          : ctx["sentiment"],
            "event_used"         : event,
            "deadline_set"       : result["deadline"]
        })


if generate_clicked:
    if not situation.strip():
        st.error("Please describe your situation or select a Quick Fill option.")
    else:
        run_generation(situation, is_emergency=False)

if emergency_clicked:
    run_generation(situation, is_emergency=True)