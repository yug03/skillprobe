"""
File Parser — extract raw text from PDF, DOCX, or TXT.
"""
import io
import pdfplumber
from docx import Document


def extract_text(uploaded_file) -> str:
    """Extract text from a Streamlit UploadedFile object."""
    name  = uploaded_file.name.lower()
    data  = uploaded_file.read()

    if name.endswith(".pdf"):
        return _from_pdf(data)
    elif name.endswith(".docx"):
        return _from_docx(data)
    elif name.endswith(".txt"):
        return data.decode("utf-8", errors="ignore")
    else:
        raise ValueError(f"Unsupported file type: {name}")


def _from_pdf(data: bytes) -> str:
    parts = []
    with pdfplumber.open(io.BytesIO(data)) as pdf:
        for page in pdf.pages:
            t = page.extract_text()
            if t:
                parts.append(t)
    return "\n".join(parts)


def _from_docx(data: bytes) -> str:
    doc = Document(io.BytesIO(data))
    return "\n".join(p.text for p in doc.paragraphs if p.text.strip())