HireSense AI 🚀

AI-Powered Resume Screening & Interview Assistant

HireSense AI is an end-to-end AI hiring assistant that automates resume screening, semantic candidate ranking, and first-round interviews. It demonstrates a production-ready AI system design using modern NLP techniques, vector databases, and LLMs, while remaining deployable as a Streamlit application.

✨ Key Features

📄 Resume Parsing – Supports PDF, DOCX, and TXT resumes

🧠 Semantic Resume Matching – Uses embeddings instead of keyword filtering

📊 Candidate Ranking – Explainable fit score with matched & missing skills

🗣️ AI Interview Agent – Auto-generated interview questions and evaluation

⚡ Low-Latency LLM Inference – Powered by Groq

🧱 Production-Ready Architecture – Streamlit frontend + FastAPI backend design

🏗️ System Architecture

Frontend: Streamlit (UI, uploads, ranking view, interview flow)

Backend (Architecture): FastAPI (API layer, kept for production design)

AI / NLP: Sentence Transformers (embeddings)

Vector Database: ChromaDB

LLM Provider: Groq

Language: Python

For deployment on Streamlit Cloud, the app runs in Streamlit-only mode, directly invoking the core AI logic. The FastAPI layer is retained in the repository to demonstrate a scalable, production-grade backend design.

📁 Project Structure
hiresense-ai/
├── streamlit_app.py          # Streamlit entry point
├── backend/
│   └── api.py                # FastAPI backend (architecture)
├── app/
│   ├── services/
│   │   └── hiring_service.py # Core business logic
│   ├── resume_parser/
│   ├── embedding_engine/
│   ├── vector_store/
│   ├── matcher/
│   └── interview_agent/
├── data/
│   └── uploads/
├── requirements.txt
├── README.md
└── .gitignore

📊 Data Used

Type: Realistic synthetic data

Content:

AI, GenAI, Backend, Frontend, Data, MLOps, DevOps resumes

Intentional skill gaps for ranking & rejection testing

Reason: Ensures privacy, ethical AI usage, and interview-safe demos

No real personal or sensitive information is used.

▶️ Run Locally
1️⃣ Create & activate virtual environment (Python 3.10 recommended)
python -m venv venv
venv\Scripts\activate   # Windows

2️⃣ Install dependencies
pip install -r requirements.txt

3️⃣ Run Streamlit app
streamlit run streamlit_app.py

☁️ Deployment (Streamlit Cloud)

Push this repository to GitHub

Go to Streamlit Cloud → New App

Select repository and set:

Main file: streamlit_app.py

Python version: 3.10

Add Secrets:

GROQ_API_KEY = "your_groq_api_key"
GROQ_MODEL = "llama-3.1-8b-instant"


Deploy 🎉

🧠 Why FastAPI is Included

FastAPI represents the production backend layer, exposing the AI pipeline as reusable APIs.
For Streamlit Cloud deployment, the same logic is called directly due to platform constraints.

This design demonstrates real-world system thinking: separating UI, business logic, and API layers.

🎯 Use Cases

AI / GenAI internship demos

Resume screening systems

Semantic search & ranking pipelines

Interview automation prototypes

📌 Skills Demonstrated

AI system design

Semantic search & embeddings

Vector databases

LLM integration

Backend architecture

Ethical data handling

👩‍💻 Author

Usha Rani
AI / GenAI Intern Aspirant

⭐ Final Note

This project is built to be:

Interview-ready

Ethically safe

Production-inspired

Easy to deploy

If you like it, feel free to ⭐ the repo!
