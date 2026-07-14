import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {
            "role": "user",
            "content": "안녕하세요. 한국어로 한 문장만 자기소개해주세요."
        }
    ],
    temperature=0.2
)

print(response.choices[0].message.content)
