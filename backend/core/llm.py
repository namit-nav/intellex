import os
from dotenv import load_dotenv
from groq import Groq

from core.memory import get_chat_memory, add_to_chat

# -------- LOAD ENV --------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(BASE_DIR, ".env")

load_dotenv(ENV_PATH, override=True)

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found in .env file")

# -------- INIT GROQ CLIENT --------
client = Groq(api_key=api_key.strip())

# -------- CONFIG --------
DEFAULT_MODEL = "llama-3.1-8b-instant"

SYSTEM_PROMPT = """
You are Intellex AI, a professional research intelligence assistant.

Your responsibilities include:
- Company research
- Strategic analysis
- Competitive comparison
- Document understanding
- Structured business insights

Instructions:
- Provide concise but detailed responses
- Use headings and bullet points when useful
- Keep outputs professional and analytical
- Avoid unnecessary fluff
- Focus on actionable insights
"""

# -------- MAIN FUNCTION --------
def ask_llm(
    prompt: str,
    model: str = DEFAULT_MODEL,
    temperature: float = 0.7
) -> str:

    try:

        # -------- GET MEMORY --------
        memory = get_chat_memory()[-6:]

        # -------- BUILD CONVERSATION --------
        messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ]

        # Add memory safely
        for msg in memory:
            if (
                isinstance(msg, dict)
                and "role" in msg
                and "content" in msg
            ):
                messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })

        # Add current user prompt
        messages.append({
            "role": "user",
            "content": prompt
        })

        # -------- CALL GROQ --------
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature
        )

        answer = response.choices[0].message.content

        # -------- SAVE MEMORY --------
        add_to_chat("user", prompt)
        add_to_chat("assistant", answer)

        return answer

    except Exception as e:

        print("LLM ERROR:", str(e))

        return (
            "An error occurred while generating the response. "
            "Please try again."
        )