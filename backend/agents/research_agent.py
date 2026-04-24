from agents.persona_manager import get_persona_prompt
from core.llm import ask_llm
from core.prompts import research_prompt
from core.memory import set_research, is_same_company, clear_chat_memory
from core.cache import get_cache, set_cache
from tavily import TavilyClient
import os


# -------- CONFIG --------
MAX_LINKS = 10
MAX_TOTAL_TEXT = 8000

# -------- MAIN FUNCTION --------
def research_company(company, persona="research_assistant", query=None):

    if not company:
        return "Please provide a company name."

    company_clean = company.lower().strip()
    persona_clean = persona.lower().strip()
    cache_key = f"{company_clean}_{persona_clean}"

    # -------- CHAT MODE --------
    if query:
        previous = get_cache(cache_key)

        if not previous:
            return "No research context found. Generate report first."

        persona_prompt = get_persona_prompt(persona)

        chat_prompt = f"""
{persona_prompt}

You already created a research report on {company}.

STRICT RULES:
- Answer ONLY using the report below
- Do NOT use outside knowledge
- Do NOT assume or hallucinate anything
- If the answer is not clearly present, say: "Not found in report"
- Be precise and concise

REPORT:
{previous}

QUESTION:
{query}

Answer:
"""
        return ask_llm(chat_prompt)

    # -------- CACHE --------
    cached = get_cache(cache_key)
    if cached:
        return cached

    # -------- RESET CHAT --------
    if not is_same_company(company):
        clear_chat_memory()

    # -------- PERSONA --------
    persona_prompt = get_persona_prompt(persona)


    tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

    # -------- SEARCH (TAVILY) --------
    try:
        response = tavily.search(
            query=f"{company} company overview business model revenue competitors latest news",
            search_depth="advanced",
            max_results=3
            )

        results = response.get("results", [])

        if not results:
            return "Failed to fetch company data."

        collected_text = "\n\n".join([
            f"{r['title']}\n{r['content'][:500]}"
            for r in results
        ])

    except Exception as e:
        return f"Search error: {str(e)}"

    # -------- NEWS (TAVILY) --------
    try:
        news_response = tavily.search(
            query=f"{company} funding acquisitions earnings results news",
            search_depth="advanced",
            max_results=3
        )

        news_results = news_response.get("results", [])

        if news_results:
            news_text = "\nRecent News:\n"
            for n in news_results:
                news_text += f"- {n['title']}\n"

            collected_text += "\n" + news_text

    except Exception:
        pass

    MAX_INPUT_SIZE = 2000
    collected_text = collected_text[:MAX_INPUT_SIZE]

    # -------- PROMPT --------
    prompt = research_prompt(persona_prompt, company, collected_text)

    # -------- LLM --------
    result = ask_llm(prompt)

    # -------- STORE --------
    set_research(company, result)
    set_cache(cache_key, result)

    return result