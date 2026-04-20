import os
from groq import Groq
from dotenv import load_dotenv
from core.memory import get_chat_memory, add_to_chat

# -------- LOAD ENV --------
load_dotenv()

# -------- API KEY --------
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("❌ GROQ_API_KEY not loaded")

# -------- CLIENT --------
client = Groq(api_key=api_key.strip())


# -------- CONFIG --------
DEFAULT_MODEL = "llama-3.1-8b-instant"

SYSTEM_PROMPT = (
    "You are a professional AI research assistant. "
    "Provide structured, clear, and analytical answers. "
    "Avoid fluff. Use headings and bullet points when useful."
)


# -------- MAIN FUNCTION --------
def ask_llm(prompt, model=DEFAULT_MODEL, temperature=0.7):

    try:
        memory = get_chat_memory()[-6:]

        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        messages.extend(memory)
        messages.append({"role": "user", "content": prompt})

        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature
        )

        answer = response.choices[0].message.content

        add_to_chat("user", prompt)
        add_to_chat("assistant", answer)

        return answer

    except Exception as e:
        return f"❌ LLM Error: {str(e)}"