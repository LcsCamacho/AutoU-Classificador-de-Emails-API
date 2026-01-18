from pydantic import BaseModel, Field

class EmailRequest(BaseModel):
    text: str = Field(..., min_length=10, description="Conteúdo do e-mail em texto puro")

class EmailResponse(BaseModel):
    category: str
    suggested_reply: str
