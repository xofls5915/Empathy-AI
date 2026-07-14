import re

ALLOWED_WORDS = {
    "AI",
    "GPT",
    "Groq",
    "pH",
    "DNA",
    "RNA"
}

def has_foreign_text(text):
    """
    답변에 영어, 중국어, 일본어가 포함되어 있는지 검사
    """
    return bool(
        re.search(
            r"[A-Za-z\u4e00-\u9fff\u3040-\u30ff]",
            text
        )
    )