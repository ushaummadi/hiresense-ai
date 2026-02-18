import os
import uuid
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from app.models import JobRequest, RankedCandidate, InterviewStartRequest, InterviewState, InterviewMessage
from app.resume_parser.parser import parse_resume
from app.embedding_engine.embedder import Embedder
from app.vectore_store.chroma_store import ChromaStore
from app.matcher.ranker import score_candidate
from app.interview_agent.agent import build_questions, evaluate_answers

UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = FastAPI(title="HireSense AI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

embedder = Embedder()
store = ChromaStore()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/upload_resume")
async def upload_resume(file: UploadFile = File(...)):
    candidate_id = str(uuid.uuid4())
    save_path = os.path.join(UPLOAD_DIR, f"{candidate_id}_{file.filename}")
    with open(save_path, "wb") as f:
        f.write(await file.read())

    text = parse_resume(save_path)

    emb = embedder.embed([text])[0]
    store.upsert_candidate(
        candidate_id=candidate_id,
        embedding=emb,
        document=text,
        metadata={"filename": file.filename, "path": save_path}
    )
    return {"candidate_id": candidate_id, "filename": file.filename}

@app.post("/rank_candidates", response_model=list[RankedCandidate])
def rank_candidates(req: JobRequest, top_k: int = 10):
    # Use job description embedding for semantic retrieval
    q_emb = embedder.embed([req.job_description])[0]
    results = store.query(q_emb, top_k=top_k)

    ranked = []
    ids = results["ids"][0]
    docs = results["documents"][0]
    metas = results["metadatas"][0]

    for cid, doc, meta in zip(ids, docs, metas):
        s = score_candidate(doc, req.must_have_skills, req.nice_to_have_skills)
        ranked.append(RankedCandidate(
            candidate_id=cid,
            filename=meta.get("filename", "unknown"),
            fit_score=s["fit_score"],
            matched_skills=s["matched_skills"],
            missing_must_haves=s["missing_must_haves"]
        ))

    ranked.sort(key=lambda x: x.fit_score, reverse=True)
    return ranked

@app.post("/interview/start")
def interview_start(req: InterviewStartRequest):
    questions = build_questions(req.job_title, req.job_description)
    state = InterviewState(
        candidate_id=req.candidate_id,
        messages=[InterviewMessage(role="assistant", content=questions[0])]
    )
    return {"state": state, "all_questions": questions}

@app.post("/interview/answer")
def interview_answer(state: InterviewState, answer: str, q_index: int, all_questions: list[str]):
    # append user answer
    state.messages.append(InterviewMessage(role="user", content=answer))

    # next question or evaluation
    if q_index + 1 < len(all_questions):
        state.messages.append(InterviewMessage(role="assistant", content=all_questions[q_index + 1]))
        return {"state": state, "done": False}

    # evaluate
    answers = [m.content for m in state.messages if m.role == "user"]
    state.evaluation = evaluate_answers(answers)
    return {"state": state, "done": True}
