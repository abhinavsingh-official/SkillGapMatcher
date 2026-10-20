"""The actual differentiator over the vendored pydparser base: a skills-gap
breakdown (which specific required skills are present vs. missing), not
just one similarity score. pydparser's own MatchingEngine computes
intersection/Jaccard/cosine scores but never surfaces *which* skills drove
them - this module parses once, reuses those same three scoring
approaches, and adds the missing piece."""

import io
import sys
from dataclasses import dataclass
from pathlib import Path

# The vendored pydparser package lives under vendor/ (see
# vendor/pydparser/ATTRIBUTION.md) rather than being pip-installed, so its
# directory needs to be on sys.path before it can be imported as a package.
sys.path.insert(0, str(Path(__file__).resolve().parent / "vendor"))

from pydparser.job_parser import JdParser  # noqa: E402
from pydparser.resume_parser import ResumeParser  # noqa: E402
from sklearn.feature_extraction.text import TfidfVectorizer  # noqa: E402
from sklearn.metrics.pairwise import cosine_similarity  # noqa: E402


@dataclass
class MatchResult:
    candidate_name: str | None
    job_occupation: str | None
    matched_skills: list[str]
    missing_skills: list[str]
    extra_skills: list[str]
    intersection_score: float
    jaccard_score: float
    cosine_score: float


def _as_file(text: str, name: str) -> io.BytesIO:
    buffer = io.BytesIO(text.encode("utf-8"))
    buffer.name = name
    return buffer


def _normalize(skills: list[str] | None) -> set[str]:
    return {s.lower().strip() for s in (skills or []) if s and s.strip()}


def analyze(resume_text: str, jd_text: str) -> MatchResult:
    resume_file = _as_file(resume_text, "resume.txt")
    jd_file = _as_file(jd_text, "jd.txt")

    resume_data = ResumeParser(resume_file).get_extracted_data()
    jd_data = JdParser(jd_file).get_extracted_data()

    resume_skills = _normalize(resume_data.get("skills"))
    job_skills = _normalize(jd_data.get("skills"))

    matched = job_skills & resume_skills
    missing = job_skills - resume_skills
    extra = resume_skills - job_skills

    intersection_score = len(matched) / len(job_skills) if job_skills else 0.0

    union = job_skills | resume_skills
    jaccard_score = len(matched) / len(union) if union else 0.0

    cosine_score = 0.0
    if job_skills and resume_skills:
        vectorizer = TfidfVectorizer()
        vectors = vectorizer.fit_transform([" ".join(job_skills), " ".join(resume_skills)])
        cosine_score = float(cosine_similarity(vectors[0:1], vectors[1:2])[0, 0])

    return MatchResult(
        candidate_name=resume_data.get("name"),
        job_occupation=jd_data.get("occupation"),
        matched_skills=sorted(matched),
        missing_skills=sorted(missing),
        extra_skills=sorted(extra),
        intersection_score=intersection_score,
        jaccard_score=jaccard_score,
        cosine_score=cosine_score,
    )
