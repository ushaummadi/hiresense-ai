import os
import uuid
from app.resume_parser.parser import parse_resume
from app.embedding_engine.embedder import Embedder
from app.vectore_store.chroma_store import ChromaStore
from app.matcher.ranker import score_candidate
from app.interview_agent.agent import build_questions, evaluate_answers

UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

embedder = Embedder()
store = ChromaStore()

def upload_resume(file_bytes, filename):
    candidate_id = str(uuid.uuid4())
    path = os.path.join(UPLOAD_DIR, f"{candidate_id}_{filename}")

    with open(path, "wb") as f:
        f.write(file_bytes)

    text = parse_resume(path)
    emb = embedder.embed([text])[0]

    store.upsert_candidate(
        candidate_id=candidate_id,
        embedding=emb,
        document=text,
        metadata={"filename": filename}
    )
    return candidate_id

def rank(job_desc, must_have, nice_to_have, top_k=10):
    q_emb = embedder.embed([job_desc])[0]
    results = store.query(q_emb, top_k=top_k)

    ranked = []
    for cid, doc, meta in zip(
        results["ids"][0],
        results["documents"][0],
        results["metadatas"][0]
    ):
        s = score_candidate(doc, must_have, nice_to_have)
        ranked.append({
            "candidate_id": cid,
            "filename": meta.get("filename", ""),
            "fit_score": s["fit_score"],
            "matched_skills": s["matched_skills"],
            "missing_must_haves": s["missing_must_haves"],
        })

    return sorted(ranked, key=lambda x: x["fit_score"], reverse=True)

def start_interview(job_title, job_desc):
    return build_questions(job_title, job_desc)

def finish_interview(answers):
    return evaluate_answers(answers)
