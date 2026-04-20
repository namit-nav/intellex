import os
from groq import Groq
from dotenv import load_dotenv
from core.memory import get_chat_memory, add_to_chat
import streamlit as st

# -------- LOAD ENV --------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(BASE_DIR, ".env")

load_dotenv(ENV_PATH, override=True)

# -------- API KEY --------

api_key = os.getenv("GROQ_API_KEY") or st.secrets["GROQ_API_KEY"]

if not api_key:
    raise ValueError("❌ GROQ_API_KEY not loaded")

api_key = api_key.strip()

# -------- CLIENT --------
client = Groq(api_key=api_key)


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
        # Get limited memory
        memory = get_chat_memory()[-6:]

        # Build messages
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        messages.extend(memory)
        messages.append({"role": "user", "content": prompt})

        # Call LLM
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature
        )

        answer = response.choices[0].message.content

        # Save memory
        add_to_chat("user", prompt)
        add_to_chat("assistant", answer)

        return answer

    except Exception as e:
        return f"❌ LLM Error: {str(e)}"