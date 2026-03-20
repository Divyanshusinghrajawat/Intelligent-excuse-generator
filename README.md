# 🎭 Intelligent Excuse Generator
> An AI-powered, NLP-driven Python application that generates context-aware,
> realistic and customizable excuses — with believability scoring, proof
> suggestions, and multi-format output.

---

## 📌 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [How It Works](#how-it-works)
- [Project Structure](#project-structure)
- [Tech Stack](#tech-stack)
- [Setup & Installation](#setup--installation)
- [How to Use](#how-to-use)
- [ML Model Details](#ml-model-details)
- [Output Formats](#output-formats)
- [Future Scope](#future-scope)
- [Author](#author)

---

## 📖 Overview

The **Intelligent Excuse Generator** is a Python-based AI application
that helps users generate realistic, context-aware excuses for different
life situations — academic, professional, social, and emergency.

Unlike simple text generators, this system uses a **hybrid approach**:
- A **rule-based NLP engine** (spaCy + NLTK) that understands the
  user's situation and extracts meaningful context
- A **template library** of 30+ professionally written excuse templates
  mapped to category, relationship and tone
- A **scikit-learn ML classifier** that scores how believable the
  generated excuse is on a scale of 1 to 10
- A clean **Jupyter Notebook UI** built with ipywidgets — no web
  framework needed, runs fully offline

The entire system works **100% offline** — no API keys, no internet
connection required after initial setup.

---

## ✨ Features

### 1. Context-Aware Excuse Generation
The system does not just pick a random excuse. It analyzes your situation
text using NLP to extract keywords, detect urgency, infer what action was
missed, and selects the most appropriate template from the library.

### 2. NLP Preprocessing (spaCy + NLTK)
- Named entity recognition (identifies people, places, dates)
- Part-of-speech tagging (extracts nouns, verbs, adjectives)
- Urgency detection (flags words like "emergency", "deadline", "ASAP")
- VADER sentiment analysis (adjusts excuse tone based on emotional context)

### 3. Rule-Based Excuse Engine
- 30+ templates organized by category and relationship type
- Dynamic placeholder filling ({event}, {action}, {deadline} etc.)
- Auto-generates realistic deadlines, recovery actions and events
- Falls back gracefully when context is ambiguous

### 4. ML Believability Scorer
- TF-IDF vectorizer + Logistic Regression pipeline
- Trained on 45 labeled excuse samples (3 classes)
- Scores excuses: Low (1–4) · Medium (5–7) · High (8–10)
- Gives actionable feedback tips to improve weak excuses
- Model saved as `.pkl` file — loads instantly on next run

### 5. Emergency Mode
- Single red button — no configuration needed
- Instantly generates a professional emergency excuse
- Works even if the situation box is empty

### 6. Multi-Format Output
Same excuse, three different formats:
- **Plain** — simple paragraph with greeting and sign-off
- **Formal Letter** — full letter with date, subject, recipient, closing
- **WhatsApp** — short, casual, emoji-friendly message

### 7. Proof & Evidence Suggestions
- Suggests 1–5 realistic supporting documents based on the event type
- Detects event type automatically (medical, technical, travel, family)
- Includes a clear ethical disclaimer

### 8. Quick Fill Templates
- 16 prebuilt situation templates across all 4 categories
- Selecting one auto-fills the situation box instantly
- Can still be edited manually after selection
- Quick fill options update dynamically when category changes

---

## ⚙️ How It Works
```
User Input (situation text + dropdowns)
            │
            ▼
    NLP Engine (spaCy)
    ├── Extract keywords (nouns, verbs, entities)
    ├── Detect urgency
    ├── Infer missed action
    └── Analyze sentiment
            │
            ▼
    Excuse Engine (Rule-based)
    ├── Select category + relationship template
    ├── Pick fitting event + recovery action
    ├── Fill placeholders with NLP context
    └── Generate raw excuse text
            │
            ├──────────────────────────────────┐
            ▼                                  ▼
    ML Scorer (scikit-learn)          Formatter
    ├── TF-IDF vectorize              ├── Plain format
    ├── Predict believability class   ├── Formal letter
    ├── Map to score (1–10)           └── WhatsApp format
    └── Generate feedback tip
            │
            ▼
    Proof Generator
    ├── Detect event type (medical/technical/travel/family)
    └── Return relevant evidence suggestions
            │
            ▼
    Jupyter Notebook UI (ipywidgets)
    └── Display all outputs in formatted HTML panel
```

---

## 📁 Project Structure
```
intelligent_excuse_generator/
│
├── 📓 Intelligent_Excuse_Generator.ipynb   ← Run this file
│
├── 📄 requirements.txt                     ← All Python dependencies
├── 📄 README.md                            ← You are here
│
├── 📁 src/                                 ← Backend Python modules
│   ├── __init__.py
│   ├── nlp_engine.py        ← spaCy NLP: keyword extraction,
│   │                           urgency detection, sentiment analysis
│   ├── excuse_engine.py     ← Rule-based generation: template
│   │                           selection and placeholder filling
│   ├── scorer.py            ← scikit-learn ML pipeline:
│   │                           TF-IDF + Logistic Regression
│   ├── formatter.py         ← Output formatting: plain, formal
│   │                           letter, WhatsApp
│   └── proof_generator.py   ← Evidence suggestions based on
│                               event type detection
│
├── 📁 data/                                ← JSON data files
│   ├── templates.json       ← 30+ excuse templates organized
│   │                           by category and relationship
│   └── training_data.json   ← 45 labeled samples for ML
│                               believability scorer training
│
├── 📁 models/                              ← Saved ML model
│   └── scorer_model.pkl     ← Trained pipeline (auto-generated
│                               on first run, reused after)
│
├── 📁 outputs/                             ← Exported excuse files
└── 📁 assets/                              ← Images and styling
```

---

## 🛠️ Tech Stack

| Component         | Technology                          | Purpose                          |
|-------------------|-------------------------------------|----------------------------------|
| Language          | Python 3.12                         | Core programming language        |
| NLP               | spaCy `en_core_web_sm`              | Keyword extraction, POS tagging  |
| Sentiment         | NLTK VADER                          | Tone and sentiment analysis      |
| ML Classifier     | scikit-learn                        | Believability scoring pipeline   |
| Vectorizer        | TF-IDF (sklearn)                    | Text feature extraction for ML   |
| UI Framework      | ipywidgets                          | Interactive notebook UI          |
| Notebook          | Jupyter Notebook                    | Delivery format                  |
| Data Format       | JSON                                | Template and training data store |
| Environment       | Python venv (.venv)                 | Dependency isolation             |

---

## ⚡ Setup & Installation

### Prerequisites
- Ubuntu / any Linux distro (or Windows with WSL)
- Python 3.10 or above
- Git (optional)

### Step 1 — Get the project
```bash
cd ~
# If using git:
git clone <repo-url>
# Or just navigate to the folder if already downloaded:
cd intelligent_excuse_generator
```

### Step 2 — Create virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```
You will see `(.venv)` at the start of your terminal — this means
the environment is active.

### Step 3 — Install all dependencies
```bash
pip install -r requirements.txt
```
This installs spaCy, NLTK, scikit-learn, ipywidgets, and Jupyter.
Takes 2–3 minutes on first run.

### Step 4 — Download spaCy language model
```bash
python -m spacy download en_core_web_sm
```

### Step 5 — Launch the notebook
```bash
jupyter notebook Intelligent_Excuse_Generator.ipynb \
  --NotebookApp.token='' --NotebookApp.password=''
```
The notebook will open in your browser automatically at
`http://localhost:8888`

---

## 🎮 How to Use

Once the notebook is open in your browser:

**Step 1 — Run all cells**
Click `Kernel → Restart & Run All` to initialize the system.
Wait for the "✅ System ready!" message in Cell 2.

**Step 2 — Select a prebuilt situation (Quick Fill)**
Use the Quick Fill dropdown to pick a prebuilt situation.
The situation box auto-fills. You can edit it manually too.

**Step 3 — Configure your excuse**

| Setting      | Options                                              |
|--------------|------------------------------------------------------|
| Category     | Academic · Professional · Social · Emergency         |
| Recipient    | Teacher · Boss · Parent · Friend · Colleague · Client · Partner |
| Tone         | Formal · Casual                                      |
| Format       | Plain · Formal Letter · WhatsApp                     |
| Proof tips   | 1 to 5 suggestions (slider)                          |

**Step 4 — Generate**
- Click **✨ Generate Excuse** for a tailored, context-aware excuse
- Click **🚨 Emergency Mode** for an instant excuse with no setup

**Step 5 — Read your output**

The output panel shows:
- The formatted excuse (plain / letter / WhatsApp)
- Believability score out of 10 with a color indicator
- Feedback tip to improve the excuse if needed
- Proof and evidence suggestions relevant to your situation

---

## 📊 ML Model Details

The believability scorer is a scikit-learn pipeline trained on
synthetic excuse data.
```
Pipeline:
  TfidfVectorizer(ngram_range=(1,2), max_features=5000)
        │
        ▼
  LogisticRegression(max_iter=1000, C=1.0, solver='lbfgs')
```

| Detail           | Value                                      |
|------------------|--------------------------------------------|
| Algorithm        | Logistic Regression                        |
| Features         | TF-IDF unigrams and bigrams                |
| Training samples | 45 labeled excuse texts                    |
| Classes          | 0 = Low · 1 = Medium · 2 = High            |
| Test accuracy    | ~77.8%                                     |
| Model file       | `models/scorer_model.pkl`                  |
| First run        | Trains and saves model automatically       |
| Subsequent runs  | Loads saved model instantly                |

### Score Bands
| Score  | Label  | Meaning                                        |
|--------|--------|------------------------------------------------|
| 8–10   | High   | Specific, verifiable, highly convincing        |
| 5–7    | Medium | Reasonable but could use more concrete details |
| 1–4    | Low    | Vague or unconvincing — needs improvement      |

---

## 📝 Output Formats

### Plain
```
Respected Sir/Ma'am,

Due to an unforeseen medical emergency, I was unable to submit
the assignment on time. I have notified the relevant parties
and request a brief extension until Friday, 21 March 2026.

Thank you for your consideration. I remain fully committed
to my responsibilities.

Divyanshu
```

### Formal Letter
```
=======================================================
                    FORMAL LETTER
=======================================================
Date    : 20 March 2026
To      : The Class Teacher / Professor
Subject : Explanation for Absence / Delay
-------------------------------------------------------

Respected Sir/Ma'am,

Due to an unforeseen medical emergency ...

Yours sincerely,
Divyanshu
=======================================================
```

### WhatsApp
```
Sir/Ma'am really sorry to message like this 🙏

Due to an unforeseen medical emergency, I was unable
to submit the assignment on time.

Will update you soon 🙏
```

---

## 🔮 Future Scope

- **Larger training dataset** — more samples for higher ML accuracy
- **LLM integration** — plug in Anthropic/OpenAI API when online
  for dynamic, truly unique excuse generation
- **Hindi and regional language support** — multilingual excuses
- **PDF export** — download excuse as a formatted PDF document
- **Streamlit web app** — browser-based UI without Jupyter
- **Excuse history** — save and revisit previously generated excuses
- **Custom templates** — let users add their own excuse templates

---

## ⚠️ Disclaimer

This project is built purely for educational purposes to demonstrate
NLP, prompt engineering, and automated text generation techniques.
The authors do not encourage dishonesty or misuse of generated content.
Always provide genuine documentation when required.

---

## 👨‍💻 Author

**Divyanshu**
B.Tech Computer Science (2nd Year)
Internship Capstone Project

Built with Python · spaCy · NLTK · scikit-learn · ipywidgets · Jupyter

---

*If you found this project useful, consider starring the repository!*
