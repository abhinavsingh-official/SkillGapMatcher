# SkillGapMatcher

An ATS-style resume-to-job-description matcher that shows its work instead of
handing back one opaque similarity number.

## Why this exists

Most resume-matching tools score a resume against a job description and stop
there — "72% compatible," with no way to tell *which* 28% is missing. That's
not useful to a candidate deciding what to add to a resume, or to a recruiter
deciding whether a gap is a dealbreaker. This tool parses both documents and
reports three real similarity scores *and* the actual skill-level
breakdown behind them: what matched, what the job wants that the resume
doesn't show, and what's on the resume that the job never asked for.

## Screenshots

![Match results](screenshots/match.png)

## How it works

1. Paste a resume and a job description as plain text (a sample pair is
   pre-filled so the app is usable immediately — no file upload required to
   try it).
2. `matcher.py` takes the two skill sets and computes:
   - **Required skills covered** — matched skills ÷ all skills the JD asks for.
   - **Jaccard similarity** — matched skills ÷ the union of both skill sets.
   - **TF-IDF cosine similarity** — vectorizes each skill set and compares them.
3. The skills-gap breakdown — **matched**, **missing**, **extra** — is the
   actual differentiator over the base library, which computes similarity
   scores but never surfaces which specific skills drove them.

## Running it locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
python -c "import nltk; nltk.download('stopwords')"
streamlit run app.py
```

## Tests

```bash
python -m pytest tests/ -v
```

## Project structure

```
app.py                  Streamlit UI
matcher.py              Scoring + skills-gap logic (the actual differentiator)
vendor/pydparser/       Vendored parsing library (MIT, see ATTRIBUTION.md)
tests/test_matcher.py   Unit tests, including the documented limitation above
```

