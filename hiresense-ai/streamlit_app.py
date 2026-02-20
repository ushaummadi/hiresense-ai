import streamlit as st

from app.services.hiring_services import (
    upload_resume,
    rank,
    start_interview,
    finish_interview,
)

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(
    page_title="HireSense AI",
    layout="wide",
)

st.title("HireSense AI — Resume Screening & Interview Agent")

tab1, tab2 = st.tabs(["📄 Upload + Rank", "🗣️ AI Interview"])

# =====================================================
# TAB 1: UPLOAD + RANK
# =====================================================
with tab1:
    st.subheader("1️⃣ Upload Resumes")

    uploaded_files = st.file_uploader(
        "Upload resumes (PDF / DOCX / TXT)",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=True,
    )

    if st.button("Upload Resumes"):
        if not uploaded_files:
            st.warning("Please upload at least one resume.")
        else:
            for f in uploaded_files:
                try:
                    if f.size == 0:
                        st.error(f"{f.name} is empty.")
                        continue

                    candidate_id = upload_resume(f.getvalue(), f.name)
                    st.success(f"Uploaded: {f.name} | Candidate ID: {candidate_id}")

                except Exception as e:
                    st.error(f"Failed to upload {f.name}: {str(e)}")

    st.divider()

    st.subheader("2️⃣ Rank Candidates")

    job_title = st.text_input("Job Title", "AI Engineer Intern")
    job_description = st.text_area(
        "Job Description",
        "Looking for Python, Machine Learning, FastAPI, vector databases, and basic LLM knowledge.",
        height=120,
    )

    must_have = st.text_input(
        "Must-have skills (comma separated)",
        "Python, Machine Learning, FastAPI, SQL",
    )

    nice_to_have = st.text_input(
        "Nice-to-have skills (comma separated)",
        "ChromaDB, LangChain, Docker, AWS",
    )

    top_k = st.slider("Top K Candidates", 3, 30, 10)

    if st.button("Rank Candidates"):
        try:
            ranked = rank(
                job_description,
                [x.strip() for x in must_have.split(",") if x.strip()],
                [x.strip() for x in nice_to_have.split(",") if x.strip()],
                top_k=top_k,
            )

            if ranked:
                st.dataframe(ranked, use_container_width=True)
            else:
                st.warning("No candidates found. Upload resumes first.")

        except Exception as e:
            st.error(f"Ranking failed: {str(e)}")

# =====================================================
# TAB 2: AI INTERVIEW
# =====================================================
with tab2:
    st.subheader("🗣️ AI Interview")

    job_title_i = st.text_input("Job Title (Interview)", "AI Engineer Intern")
    job_description_i = st.text_area(
        "Job Description (Interview)",
        "Looking for Python, Machine Learning, FastAPI, vector databases, and LLM basics.",
        height=120,
        key="jd_interview",
    )

    # Session state initialization
    if "questions" not in st.session_state:
        st.session_state.questions = []
        st.session_state.answers = []
        st.session_state.q_index = 0
        st.session_state.interview_done = False
        st.session_state.evaluation = None

    if st.button("Start Interview"):
        try:
            st.session_state.questions = start_interview(
                job_title_i,
                job_description_i,
            )
            st.session_state.answers = []
            st.session_state.q_index = 0
            st.session_state.interview_done = False
            st.session_state.evaluation = None
            st.success("Interview started!")
        except Exception as e:
            st.error(f"Interview failed to start: {str(e)}")
    if st.session_state.questions and not st.session_state.interview_done:
        current_q = st.session_state.questions[st.session_state.q_index]
        st.info(f"Question {st.session_state.q_index + 1}: {current_q}")

        answer = st.text_area("Your Answer", key=f"ans_{st.session_state.q_index}")

        if st.button("Submit Answer"):
            if not answer.strip():
                st.warning("Please enter your answer before submitting.")
            else:
                st.session_state.answers.append(answer)

                if st.session_state.q_index + 1 < len(st.session_state.questions):
                    st.session_state.q_index += 1
                    st.rerun()
                else:
                    evaluation = finish_interview(st.session_state.answers)
                    st.session_state.evaluation = evaluation 
                    st.session_state.interview_done = True
                    st.success("Interview Completed!")
                    st.rerun()
    if st.session_state.interview_done and st.session_state.evaluation:

        evaluation = st.session_state.evaluation
        score = evaluation.get("communication_score_10", 0)

        st.subheader("📊 Interview Evaluation")

        # Progress Bar
        st.progress(score / 10)

        # Score Metric
        st.metric(
            label="Communication Score",
            value=f"{score} / 10"
        )

        # Feedback
        st.success(evaluation.get("notes", "Evaluation complete."))

        # Optional Raw JSON Toggle
        with st.expander("🔎 View Raw Evaluation JSON"):
            st.json(evaluation)

        # Restart Button
        if st.button("🔄 Restart Interview"):
            st.session_state.questions = []
            st.session_state.answers = []
            st.session_state.q_index = 0
            st.session_state.interview_done = False
            st.session_state.evaluation = None
            st.experimental_rerun()

    elif st.session_state.interview_done:
        st.info("Interview already completed. Restart to try again.")


