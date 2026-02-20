from typing import List, Dict
from app.config import GROQ_API_KEY, GROQ_MODEL
import requests
import json

# ----------------------------------------
# Question Builder (MVP Safe)
# ----------------------------------------

def build_questions(job_title: str, job_description: str) -> List[str]:
    return [
        f"Tell me about a project where you used skills relevant to {job_title}. What was your role?",
        "Explain one challenging bug or issue you solved. How did you debug it?",
        "How do you ensure your code is clean and maintainable? Any examples?",
        "If you had to improve performance of an API/model, what steps would you take?",
        "Why should we hire you for this role?"
    ]


# ----------------------------------------
# Heuristic Evaluation (Fallback Safe)
# ----------------------------------------

def heuristic_score(answers: List[str]) -> float:
    length_scores = [min(len(a.split()) / 60, 1.0) for a in answers]
    return round(sum(length_scores) / max(1, len(length_scores)) * 10, 1)


# ----------------------------------------
# LLM Evaluation Using Groq
# ----------------------------------------

def llm_evaluate(transcript: str) -> Dict:
    prompt = f"""
You are an interview evaluator.

Evaluate the following interview answers for:

1. Communication clarity
2. Relevance to the role
3. Completeness
4. Confidence

Return STRICT JSON only in this format:

{{
    "communication_score_10": <number between 1 and 10>,
    "notes": "<short evaluation feedback>"
}}

Interview Answers:
{transcript}
"""

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": GROQ_MODEL,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.2
        },
        timeout=30
    )

    result = response.json()
    content = result["choices"][0]["message"]["content"]

    # Safe JSON parsing
    try:
        return json.loads(content)
    except:
        return {
            "communication_score_10": 0,
            "notes": "LLM response parsing failed."
        }


# ----------------------------------------
# Main Evaluation Function
# ----------------------------------------

def evaluate_answers(answers: List[str]) -> Dict:

    if not answers:
        return {
            "communication_score_10": 0,
            "notes": "No answers provided."
        }

    transcript = "\n".join(answers)

    # If no API key → fallback to heuristic
    if not GROQ_API_KEY:
        score = heuristic_score(answers)
        return {
            "communication_score_10": score,
            "notes": "Heuristic evaluation (LLM disabled)."
        }

    try:
        llm_result = llm_evaluate(transcript)
        if isinstance(llm_result, list):
            llm_result = llm_result[0] if llm_result else {}

        # Optional Hybrid Score
        heuristic = heuristic_score(answers)
        llm_score = llm_result.get("communication_score_10", 0)

        final_score = round((heuristic * 0.3) + (llm_score * 0.7), 1)

        return {
            "communication_score_10": final_score,
            "notes": llm_result.get("notes", "LLM evaluation complete.")
        }

    except Exception as e:
        return {
            "communication_score_10": heuristic_score(answers),
            "notes": f"Fallback to heuristic. Error: {str(e)}"
        }


# ----------------------------------------
# Optional LLM Summary Feature
# ----------------------------------------

def llm_summary(transcript: str) -> str:

    if not GROQ_API_KEY:
        return "LLM summary disabled (no GROQ_API_KEY)."

    prompt = f"""
Summarize this interview transcript in 5 lines with strengths and improvement areas.

Transcript:
{transcript}
"""

    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": GROQ_MODEL,
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.3
            },
            timeout=30
        )

        result = response.json()
        return result["choices"][0]["message"]["content"]

    except:
        return "LLM summary generation failed."

