import math
import gradio as gr
import ollama
import re

def korean_filter(text):

    # 영어 제거
    text = re.sub(r'[A-Za-z]+', '', text)

    # 중국어/일본어 제거
    text = re.sub(
        r'[\u4e00-\u9fff\u3040-\u30ff]',
        '',
        text
    )

    return text.strip()


# ===========================
# Danger Detector
# ===========================

class DangerDetector:

    def __init__(self):
        self.score = 0

        self.rules = {
            "힘들":1,
            "지쳤":1,
            "무기력":1,
            "외롭":2,
            "혼자":2,
            "죽":2,
            "사라":2,
            "방법":3,
            "계획":3
        }

    def update(self, text):

        for word, weight in self.rules.items():

            if word in text:
                self.score += weight

        self.score = min(self.score,10)

        return self.score


danger = DangerDetector()
class SafetyGovernor:

    def mode(self, D):

        if D >= 7:
            return "SAFETY"

        return "NORMAL"

    def safety_message(self):

        return (
            "현재 위험도가 높게 감지되었습니다.\n"
            "혼자 감당하려 하지 말고 가까운 사람과 이야기해보세요."
        )

governor = SafetyGovernor()
###############################################
# Prompt Generator
###############################################

def build_prompt(user_message, empathy_score, danger_score):

    prompt = f"""
너는 '공감 안전장치(Empathy Safety Governor)'를 적용한 생성형 AI이다.

현재 계산값

Danger Index : {danger_score}/10

Empathy Score : {round(empathy_score,3)}

규칙

1. 먼저 감정을 인정한다.
2. 해결책을 서두르지 않는다.
3. 공감 강도는 Empathy Score에 맞춘다.
4. 위험도가 높을수록 차분하고 신중하게 답한다.
5. 위험한 감정에 동조하지 않는다.
6. 답변은 3~5문장으로 작성한다.
7. 최종 출력은 반드시 한국어 문장으로만 작성한다.
8. 출력 전에 외국어 표현이 있는지 스스로 확인하고 한국어 표현으로 수정한다.

사용자

{user_message}
"""

    return prompt


# ===========================
# Empathy Model
# ===========================

def theta(D):
    return 4 + 0.2*D


def ceiling(D):
    return max(0,1-0.04*D)


def empathy(I,R,D):

    return ceiling(D)/(1+math.exp(-(I*R-theta(D))))


# ===========================
# GPT
# ===========================

SYSTEM = """
너는 한국어 전용 상담 AI이다.

절대 영어 알파벳을 출력하지 않는다.
절대 영어 단어를 사용하지 않는다.
전문 용어도 가능한 경우 한국어 표현으로 바꾼다.

금지 예:
Good, Sorry, OK, Thank you, AI, Emotion, Stress

허용:
좋아요, 미안해요, 괜찮아요, 고마워요, 인공지능, 감정, 스트레스

답변 생성 후 반드시 스스로 검사한다.

만약 영어가 포함되면 다시 작성한다.

모든 답변은 3~5개의 한국어 문장으로 작성한다.
"""


def ask_gpt(user_message, empathy_score, danger_score):

    prompt = build_prompt(
        user_message,
        empathy_score,
        danger_score
    )

    response = ollama.chat(

        model="exaone3.5",

        options={
            "temperature":0.0
        },

        messages=[

            {
                "role":"system",
                "content":SYSTEM
            },

            {
                "role":"user",
                "content":prompt
            }

        ]

    )

    answer = response["message"]["content"]

    answer = korean_filter(answer)

    return answer
###############################################
# Main Engine
###############################################

def run_ai(user_message):

    D = danger.update(user_message)

    I = min(len(user_message)//8 + 1, 10)

    keywords = [
        "나","내","나는","내가","내 인생","내 미래"
    ]

    R = 1

    for k in keywords:
        if k in user_message:
            R += 2

    R = min(R,10)

    E = empathy(I,R,D)

    mode = governor.mode(D)

    if mode == "SAFETY":

        return {
            "answer": governor.safety_message(),
            "danger": D,
            "empathy": E,
            "mode": mode
        }

    answer = ask_gpt(
        user_message,
        E,
        D
    )

    return {
        "answer": answer,
        "danger": D,
        "empathy": E,
        "mode": mode
    }
###############################################
# Gradio UI
###############################################

def chat(user_message, history):

    result = run_ai(user_message)

    answer = result["answer"]

    info = (
        f"⚠ Danger Index : {result['danger']}\n"
        f"❤️ Empathy Score : {round(result['empathy'],3)}\n"
        f"🛡 Mode : {result['mode']}"
    )

    new_history = history.copy()

    new_history.append({
        "role": "user",
        "content": user_message
    })

    new_history.append({
        "role": "assistant",
        "content": answer
    })

    return new_history, info


with gr.Blocks(title="Empathy AI") as demo:

    gr.Markdown("# 🤖 Empathy AI")

    chatbot = gr.Chatbot()

    debug = gr.Textbox(
        label="Empathy Engine",
        lines=5
    )

    msg = gr.Textbox(
        label="메시지 입력"
    )


    msg.submit(
        fn=chat,
        inputs=[msg, chatbot],
        outputs=[chatbot, debug]
    )

if __name__ == "__main__":

    print("Start")

    demo.launch(inbrowser=True)