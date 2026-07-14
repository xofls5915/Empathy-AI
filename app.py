
import gradio as gr
from engine import run_ai

###############################################
# Gradio UI
###############################################

def chat(user_message, history):

    result = run_ai(user_message, history)

    answer = result["answer"]

    info = (
        f"⚠ Danger Index : {result['danger']}\n"
        f"├ Keyword : {result['keyword']}\n"
        f"├ Emotion : {result['emotion']}\n"
        f"└ Intensity : {result['intensity']}\n\n"
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

