# SkillGapMatcher

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) ![spaCy](https://img.shields.io/badge/spaCy-09A3D5?style=for-the-badge&logo=spacy&logoColor=white) ![scikit--learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white) ![NLTK](https://img.shields.io/badge/NLTK-154F3C?style=for-the-badge) ![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)

An ATS-style resume-to-job-description matcher that shows its work instead
of handing back one opaque similarity number. It parses both documents with
NER and reports three real similarity scores alongside the actual
skill-level breakdown behind them - what matched, what the job wants that
the resume doesn't show, and what's on the resume the job never asked for.

## Screenshots

![Match results](screenshots/match.png)

## How to run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
python -c "import nltk; nltk.download('stopwords')"
streamlit run app.py
```

Tests: `python -m pytest tests/ -v`
