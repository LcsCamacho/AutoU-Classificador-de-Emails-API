import io
import re
from nltk.corpus import stopwords
from fastapi import UploadFile
from pypdf import PdfReader
_STOPWORDS_PT = set(stopwords.words("portuguese"))

def normalize_text(text: str) -> str:
    cleaned = text.lower()
    cleaned = re.sub(r"[^a-zA-ZÀ-ÿ0-9\s]", " ", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned

def remove_stopwords(text: str) -> str:
    tokens = text.split()
    filtered = [t for t in tokens if t not in _STOPWORDS_PT]
    return " ".join(filtered)

def preprocess_email_text(raw_text: str) -> str:
    normalized = normalize_text(raw_text)
    without_stopwords = remove_stopwords(normalized)
    return without_stopwords

async def extract_text_from_txt(file: UploadFile) -> str:
    content_bytes = await file.read()
    try:
        return content_bytes.decode("utf-8", errors="ignore")
    finally:
        await file.close()

async def extract_text_from_pdf(file: UploadFile) -> str:
    content_bytes = await file.read()
    try:
        pdf_stream = io.BytesIO(content_bytes)
        reader = PdfReader(pdf_stream)
        texts = [page.extract_text() or "" for page in reader.pages]
        return "\n".join(texts)
    finally:
        await file.close()