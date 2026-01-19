from typing import Literal

Category = Literal["produtivo", "improdutivo"]

_CATEGORIES = ("produtivo", "improdutivo")

def build_classification_system_prompt() -> str:
    return (
        "Você é um assistente especializado em triagem de e-mails corporativos "
        "de uma empresa do setor financeiro."
    )

def build_classification_user_prompt(email_text: str) -> str:
    categories_str = ", ".join(_CATEGORIES)
    return f"""
Classifique o e-mail em exatamente uma das categorias: {categories_str}.

Retorne APENAS a palavra da categoria, sem explicações adicionais.

E-mail:
\"{email_text}\"
"""

def build_reply_system_prompt() -> str:
    return (
        "Você é um assistente que escreve respostas de e-mail educadas e objetivas, "
        "em contexto corporativo do setor financeiro."
    )

def build_reply_user_prompt(email_text: str, category: Category) -> str:
    base_instruction = (
        "Gere uma resposta curta, educada e objetiva para o e-mail abaixo. "
        f"Considere que ele foi classificado como {category}."
    )

    if category == "improdutivo":
        base_instruction += (
            " Responda de forma simpática, gentil e agradecendo, mas sem assumir ações complexas. "
            "Você pode agradecer e encerrar a conversa, se apropriado."
        )
    else:
        base_instruction += (
            " Esclareça as dúvidas ou peça as informações mínimas necessárias "
            "para dar sequência na solicitação."
        )

    return f"""{base_instruction}

E-mail:
\"\"\"{email_text}\"\"\"
"""
