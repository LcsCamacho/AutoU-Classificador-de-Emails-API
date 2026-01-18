from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from .schemas import EmailRequest, EmailResponse
from .nlp import preprocess_email_text, extract_text_from_txt, extract_text_from_pdf
from .classifier import generate_reply, classify_email

app = FastAPI(title="Email Classifier API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/classify-email", response_model=EmailResponse)
def classify_email_endpoint(payload: EmailRequest):
    raw_text = payload.text or ""
    if len(raw_text.strip()) < 10:
        raise HTTPException(status_code=400, detail="Texto do e-mail é muito curto ou vazio.")
    
    try:
        preprocessed = preprocess_email_text(raw_text)
        category = classify_email(preprocessed)
        suggested_reply = generate_reply(preprocessed,category)
        return EmailResponse(
            category=category,
            suggested_reply=suggested_reply,
        )
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Erro ao classificar e-mail ou gerar resposta.")

@app.post("/classify-email-file", response_model=EmailResponse)
async def classify_email_file_endpoint(file: UploadFile = File(...)):
    if file.content_type not in ("text/plain", "application/pdf"):
        raise HTTPException(status_code=400, detail="Apenas arquivos .txt ou .pdf são suportados.")

    try:
        if file.content_type == "text/plain":
            raw_text = await extract_text_from_txt(file)
        else:
            raw_text = await extract_text_from_pdf(file)

        if len(raw_text.strip()) < 10:
            raise HTTPException(status_code=400, detail="Arquivo não contém texto suficiente.")

        preprocessed = preprocess_email_text(raw_text)
        category = classify_email(preprocessed)
        suggested_reply = generate_reply(preprocessed,category)
        return EmailResponse(
            category=category,
            suggested_reply=suggested_reply,
        )
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Erro ao processar arquivo ou classificar e-mail.")
