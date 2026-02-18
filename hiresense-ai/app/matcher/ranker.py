from typing import List, Dict
from app.utils import extract_skills_simple

def score_candidate(resume_text: str, must_have: List[str], nice_to_have: List[str]) -> Dict:
    matched_must = extract_skills_simple(resume_text, must_have)
    matched_nice = extract_skills_simple(resume_text, nice_to_have)

    missing_must = sorted(set(must_have) - set(matched_must), key=str.lower)

    # Simple weighted score:
    # 70% must-have coverage + 30% nice-to-have coverage
    must_score = (len(matched_must) / max(1, len(must_have))) * 70
    nice_score = (len(matched_nice) / max(1, len(nice_to_have))) * 30
    fit = round(must_score + nice_score, 2)

    return {
        "fit_score": fit,
        "matched_skills": sorted(set(matched_must + matched_nice), key=str.lower),
        "missing_must_haves": missing_must
    }
