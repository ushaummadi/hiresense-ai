from typing import List, Dict
from app.config import GROQ_API_KEY, GROQ_MODEL

def build_questions(job_title: str, job_description: str) -> List[str]:
    # Baseline: rule-based questions (good for MVP + demo)
    return [
        f"Tell me about a project where you used skills relevant to {job_title}. What was your role?",
        "Explain one challenging bug or issue you solved. How did you debug it?",
        "How do you ensure your code is clean and maintainable? Any examples?",
        "If you had to improve performance of an API/model, what steps would you take?",
        "Why should we hire you for this role?"
    ]

def evaluate_answers(answers: List[str]) -> Dict:
    # Simple heuristic scoring (replace with LLM later)
    length_scores = [min(len(a.split()) / 60, 1.0) for a in answers]  # 60+ words = good
    communication = round(sum(length_scores) / max(1, len(length_scores)) * 10, 1)

    return {
        "communication_score_10": communication,
        "notes": "Heuristic evaluation based on answer completeness. Add LLM evaluation for deeper scoring."
    }

# Optional: LLM evaluation (only if user adds GROQ_API_KEY)
def llm_summary_stub(transcript: str) -> str:
    if not GROQ_API_KEY:
        return "LLM summary disabled (no GROQ_API_KEY)."

    # Keep it simple: you can replace with official Groq client later
    # This stub avoids crashing when key is missing.
    return f"LLM summary would be generated here using {GROQ_MODEL}."
