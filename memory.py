def build_messages(system_prompt, history, current_prompt, max_history=10):

    messages = [
        {
            "role": "system",
            "content": system_prompt
        }
    ]

    for msg in history[-max_history:]:

        if isinstance(msg, dict):

            messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })

    messages.append({
        "role": "user",
        "content": current_prompt
    })

    return messages