import re
from typing import List

def normalize_text(t: str) -> str:
    t = t.replace("\x00", " ")
    t = re.sub(r"\s+", " ", t).strip()
    return t

def extract_skills_simple(text: str, skill_list: List[str]) -> List[str]:
    """Simple baseline: case-insensitive substring match with word boundaries."""
    found = []
    t = text.lower()
    for s in skill_list:
        s_norm = s.strip().lower()
        if not s_norm:
            continue
        pattern = r"\b" + re.escape(s_norm) + r"\b"
        if re.search(pattern, t):
            found.append(s)
    return sorted(set(found), key=str.lower)
