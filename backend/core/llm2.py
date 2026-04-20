import ollama
from core.memory import get_chat_memory, add_to_chat


def ask_llm(prompt):

    full_memory = get_chat_memory()

    # Use only last 6 messages for context
    limited_memory = full_memory[-6:]

    messages = [
        {
            "role": "system",
            "content": "You are a professional AI research assistant that provides clear, structured, and analytical answers."
        }
    ]

    messages.extend(limited_memory)

    messages.append({
        "role": "user",
        "content": prompt
    })

    try:
        response = ollama.chat(
            model="mistral",
            messages=messages
        )

        answer = response["message"]["content"]

        # Store properly
        add_to_chat("user", prompt)
        add_to_chat("assistant", answer)

        return answer

    except Exception:
        return "Error: Unable to generate response. Please try again."