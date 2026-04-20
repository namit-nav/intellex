import os
from groq import Groq
from dotenv import load_dotenv

from core.memory import get_chat_memory, add_to_chat

# -------- LOAD ENV --------
# FORCE correct backend .env

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ENV_PATH = os.path.join(BASE_DIR, ".env")

print("Loading ENV from:", ENV_PATH)

load_dotenv(ENV_PATH, override=True)

api_key = os.getenv("GROQ_API_KEY")

print("FINAL API KEY:", repr(api_key))

if not api_key:
    print("WARNING: GROQ_API_KEY not found")

from groq import Groq

client = Groq(api_key=api_key.strip())

# -------- CONFIG --------
DEFAULT_MODEL = "llama-3.1-8b-instant"

SYSTEM_PROMPT = (
    "You are a professional AI research assistant. "
    "Provide structured, clear, and analytical answers. "
    "Avoid fluff. Use headings and bullet points when useful."
)

# -------- MAIN FUNCTION --------
def ask_llm(prompt: str, model: str = DEFAULT_MODEL, temperature: float = 0.7) -> str:
    try:
        # Get last few messages from memory
        memory = get_chat_memory()[-6:]

        # Build conversation
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]

        # Ensure memory is valid format
        for msg in memory:
            if "role" in msg and "content" in msg:
                messages.append(msg)

        messages.append({"role": "user", "content": prompt})

        # Call Groq API
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature
        )

        answer = response.choices[0].message.content

        # Save to memory
        add_to_chat("user", prompt)
        add_to_chat("assistant", answer)

        return answer

    except Exception as e:
        print("LLM ERROR:", str(e))
        return f"Error: {str(e)}"