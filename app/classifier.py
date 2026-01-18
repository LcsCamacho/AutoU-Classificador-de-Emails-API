from typing import Tuple
from .prompts import (
    Category,
    build_classification_system_prompt,
    build_classification_user_prompt,
    build_reply_system_prompt,
    build_reply_user_prompt,
)
from .llm_client import create_chat_completion

_VALID_CATEGORIES = {"produtivo", "improdutivo"}

def classify_email(preprocessed_text: str) -> Category:
    system_prompt = build_classification_system_prompt()
    user_prompt = build_classification_user_prompt(preprocessed_text)

    input = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    raw_category = create_chat_completion(input, temperature=1).strip()

    if raw_category not in _VALID_CATEGORIES:
        return "improdutivo"

    return raw_category 

def generate_reply(original_text: str, category: Category) -> str:

    system_prompt = build_reply_system_prompt()
    user_prompt = build_reply_user_prompt(original_text, category)

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    reply = create_chat_completion(messages, temperature=1)
    return reply.strip()