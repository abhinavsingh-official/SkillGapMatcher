"""SkillGapMatcher - paste a resume and a job description, get a match
score plus an actual skills-gap breakdown: what's matched, what's
missing, what's extra. The base parsing/scoring (vendor/pydparser) only
ever produced a single similarity number; the gap breakdown is the real
addition this project makes."""

import streamlit as st

from matcher import analyze

st.set_page_config(page_title="SkillGapMatcher", layout="wide")

STYLE = """
<style>
.block-container { padding-top: 2rem; max-width: 1100px; }
h1 { font-weight: 700; letter-spacing: -0.02em; color: #2563eb; }
.sg-card {
    background: #eef2ff; border: 1px solid #c7d2fe; border-radius: 10px;
    padding: 1rem 1.2rem; margin-bottom: 0.8rem;
}
.sg-stat { font-size: 2.2rem; font-weight: 700; color: #2563eb; }
.sg-stat-label { color: #4b5563; font-size: 0.9rem; }
.sg-skill-matched {
    display: inline-block; background: #dcfce7; color: #166534; border: 1px solid #86efac;
    border-radius: 999px; padding: 0.2rem 0.7rem; margin: 0.2rem; font-size: 0.85rem;
}
.sg-skill-missing {
    display: inline-block; background: #fee2e2; color: #991b1b; border: 1px solid #fca5a5;
    border-radius: 999px; padding: 0.2rem 0.7rem; margin: 0.2rem; font-size: 0.85rem;
}
.sg-skill-extra {
    display: inline-block; background: #f3f4f6; color: #374151; border: 1px solid #d1d5db;
    border-radius: 999px; padding: 0.2rem 0.7rem; margin: 0.2rem; font-size: 0.85rem;
}
</style>
"""

SAMPLE_RESUME = """Jane Doe
Email: jane.doe@email.com

Experience:
Software Engineer, TechCorp, 2019-2024
- Built data pipelines using Python and SQL
- Deployed services with Docker

Skills: Python, SQL, Docker, Git, AWS, React, JavaScript"""

SAMPLE_JD = """We are hiring a Senior Data Engineer with strong experience in Python, SQL,
Apache Spark, and AWS. Experience with Docker and Kubernetes is a plus. Familiarity with
Airflow and Kafka is a bonus."""


def home_tab():
    st.markdown(
        '<div class="sg-card" style="padding:2rem 2.2rem;">'
        "<h2 style='margin-top:0;'>A resume-to-JD score, with the gap spelled out</h2>"
        "<p style='color:#374151; font-size:1.05rem; max-width:760px; line-height:1.6;'>"
        "Most ATS-style matchers give you one similarity number and stop there. This shows "
        "which specific skills the job actually wants that your resume is missing - not just "
        "that you're \"72% compatible.\""
        "</p>"
        "<ul>"
        "<li><b>Matched</b> - skills both the resume and job description mention</li>"
        "<li><b>Missing</b> - skills the job wants that the resume doesn't show</li>"
        "<li><b>Extra</b> - skills on the resume the job description never asked for</li>"
        "</ul>"
        "</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p style="color:#4b5563;">Head to <b>Match</b> to try it - a sample resume and job '
        "description are pre-filled so you can see it work immediately.</p>",
        unsafe_allow_html=True,
    )


def match_tab():
    col1, col2 = st.columns(2)
    with col1:
        resume_text = st.text_area("Resume (paste as plain text)", value=SAMPLE_RESUME, height=280)
    with col2:
        jd_text = st.text_area("Job description (paste as plain text)", value=SAMPLE_JD, height=280)

    if not st.button("Analyze match"):
        return

    with st.spinner("Parsing and scoring..."):
        result = analyze(resume_text, jd_text)

    st.markdown("#### Match scores")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            f'<div class="sg-card"><div class="sg-stat">{result.intersection_score:.0%}</div>'
            '<div class="sg-stat-label">Required skills covered</div></div>',
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            f'<div class="sg-card"><div class="sg-stat">{result.jaccard_score:.0%}</div>'
            '<div class="sg-stat-label">Jaccard similarity</div></div>',
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            f'<div class="sg-card"><div class="sg-stat">{result.cosine_score:.0%}</div>'
            '<div class="sg-stat-label">TF-IDF cosine similarity</div></div>',
            unsafe_allow_html=True,
        )

    if result.candidate_name or result.job_occupation:
        st.markdown(
            f'<p style="color:#4b5563;">Candidate: <b>{result.candidate_name or "not detected"}</b> '
            f'&nbsp;|&nbsp; Role: <b>{result.job_occupation or "not detected"}</b></p>',
            unsafe_allow_html=True,
        )

    st.markdown("#### Skills gap breakdown")

    def render_skills(label: str, skills: list[str], css_class: str):
        st.markdown(f"**{label}** ({len(skills)})")
        if not skills:
            st.markdown('<p style="color:#9ca3af;">None</p>', unsafe_allow_html=True)
            return
        html = "".join(f'<span class="{css_class}">{s}</span>' for s in skills)
        st.markdown(html, unsafe_allow_html=True)

    render_skills("Matched", result.matched_skills, "sg-skill-matched")
    render_skills("Missing - the job wants these, your resume doesn't show them", result.missing_skills, "sg-skill-missing")
    render_skills("Extra - on your resume, not asked for in this job", result.extra_skills, "sg-skill-extra")


def main():
    st.markdown(STYLE, unsafe_allow_html=True)
    st.title("SkillGapMatcher")
    st.caption("A resume-to-job-description matcher that shows its work, not just a score.")
    tab0, tab1 = st.tabs(["Home", "Match"])
    with tab0:
        home_tab()
    with tab1:
        match_tab()


if __name__ == "__main__":
    main()
