from typing import List, Dict
from openai import OpenAI
import logging
from .config import MODEL_NAME, OPENAI_API_KEY

logger = logging.getLogger(__name__)
Message = Dict[str, str]

def create_chat_completion(
    messages: List[Message],
    temperature: float = 0.3
) -> str:

    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY não configurada")

    client = OpenAI(api_key=OPENAI_API_KEY)

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            temperature=temperature,
        )
    except Exception as e:
        logger.exception("Erro na chamada OpenAI")
        raise RuntimeError(f"OpenAI API error: {e}")

    if not response.choices:
        raise RuntimeError("OpenAI retornou zero choices")

    message = response.choices[0].message
    if not message or not message.content:
        raise RuntimeError("Mensagem vazia do OpenAI")

    return message.content.strip()
