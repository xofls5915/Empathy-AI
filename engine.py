from detector import DangerDetector
from empathy import empathy
from governor import SafetyGovernor
from prompts import SYSTEM, build_prompt
from memory import build_messages
from llm import ask_llm


danger = DangerDetector()
governor = SafetyGovernor()


def run_ai(user_message, history):

    # 위험도 계산
    danger_result = danger.update(user_message)

    danger_score = danger_result["total"]

    # 입력 길이
    input_score = min(len(user_message) // 8 + 1, 10)

    # 자기지시성 계산
    keywords = [
        "나",
        "내",
        "나는",
        "내가",
        "내 인생",
        "내 미래"
    ]

    self_reference = 1

    for word in keywords:
        if word in user_message:
            self_reference += 2

    self_reference = min(self_reference, 10)

    empathy_score = empathy(
        input_score,
        self_reference,
        danger_score
    )
    if empathy_score >= 0.8:
        empathy_level = "매우 깊은 공감과 세심한 반응이 필요한 상태"

    elif empathy_score >= 0.5:
        empathy_level = "적절한 공감과 상황 이해가 필요한 상태"

    else:
        empathy_level = "간단한 공감과 자연스러운 대화가 필요한 상태"

    mode = governor.mode(danger_score)

    if mode == "SAFETY":

        return {
            "answer": governor.safety_message(),
            "danger": danger_score,
            "keyword": danger_result["keyword"],
            "emotion": danger_result["emotion"],
            "intensity": danger_result["intensity"],
            "empathy": empathy_score,
            "mode": mode
        }

    user_prompt = build_prompt(
        user_message,
        empathy_score,
        danger_score,
        empathy_level
    )

    messages = build_messages(
        SYSTEM,
        history,
        user_prompt
    )

    answer = ask_llm(messages)

    return {
        "answer": answer,
        "danger": danger_score,
        "keyword": danger_result["keyword"],
        "emotion": danger_result["emotion"],
        "intensity": danger_result["intensity"],
        "empathy": empathy_score,
        "mode": mode
    }