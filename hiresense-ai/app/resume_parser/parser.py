import pdfplumber
from pathlib import Path

def parse_resume(path: str):
    p = Path(path)

    if p.stat().st_size == 0:
        raise ValueError("Uploaded file is empty.")

    try:
        with pdfplumber.open(str(p)) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text

    except Exception as e:
        raise ValueError("Invalid or corrupted PDF file.")
