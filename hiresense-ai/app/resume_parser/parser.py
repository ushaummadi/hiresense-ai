from pathlib import Path
import pdfplumber
import docx

def parse_resume(path: str):
    p = Path(path)
    suffix = p.suffix.lower()

    # Empty file check
    if p.stat().st_size == 0:
        raise ValueError("Uploaded file is empty.")

    # PDF
    if suffix == ".pdf":
        try:
            text = ""
            with pdfplumber.open(str(p)) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ""
            return text.strip()
        except Exception:
            raise ValueError("Invalid or corrupted PDF file.")

    # DOCX
    elif suffix == ".docx":
        try:
            doc = docx.Document(str(p))
            return "\n".join([para.text for para in doc.paragraphs]).strip()
        except Exception:
            raise ValueError("Invalid DOCX file.")

    # TXT
    elif suffix == ".txt":
        try:
            return p.read_text(encoding="utf-8").strip()
        except Exception:
            raise ValueError("Invalid TXT file.")

    else:
        raise ValueError("Unsupported file format.")
