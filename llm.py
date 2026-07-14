import os

from dotenv import load_dotenv
from groq import Groq

from validator import has_foreign_text

# .env 읽기
load_dotenv()

# Groq 클라이언트 생성
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def ask_llm(messages):

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=0.6
    )

    answer = response.choices[0].message.content

    # 외국어가 있으면 한 번 더 생성
    if has_foreign_text(answer):

        retry_messages = messages + [
            {
                "role": "assistant",
                "content": answer
            },
            {
                "role": "user",
                "content":
                (
                    "방금 답변에 외국어가 포함되어 있습니다. "
                    "자연스러운 한국어만 사용하여 다시 작성하세요. "
                    "영어, 중국어, 일본어는 절대 사용하지 마세요."
                )
            }
        ]

        retry = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=retry_messages,
            temperature=0.1
        )

        answer = retry.choices[0].message.content

    return answer