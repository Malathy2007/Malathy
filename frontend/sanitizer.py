def sanitize_text(text: str) -> str:
    return text.replace("“", '"').replace("”", '"').strip()