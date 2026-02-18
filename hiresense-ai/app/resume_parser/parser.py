from pathlib import Path
import pdfplumber
import docx2txt
from app.utils import normalize_text

SUPPORTED = {".pdf", ".docx", ".txt"}

def parse_resume(file_path: str) -> str:
    p = Path(file_path)
    if p.suffix.lower() not in SUPPORTED:
        raise ValueError(f"Unsupported file type: {p.suffix}. Use PDF/DOCX/TXT")

    if p.suffix.lower() == ".pdf":
        text = []
        with pdfplumber.open(str(p)) as pdf:
            for page in pdf.pages:
                text.append(page.extract_text() or "")
        return normalize_text("\n".join(text))

    if p.suffix.lower() == ".docx":
        return normalize_text(docx2txt.process(str(p)) or "")

    return normalize_text(p.read_text(encoding="utf-8", errors="ignore"))
