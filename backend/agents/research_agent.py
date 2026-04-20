from concurrent.futures import ThreadPoolExecutor

from research.search import search_company
from research.web_scraper import scrape_page
from research.text_cleaner import clean_text
from research.news_collector import get_company_news

from agents.persona_manager import get_persona_prompt
from core.llm import ask_llm
from core.prompts import research_prompt
from core.memory import set_research, is_same_company, clear_chat_memory
from core.cache import get_cache, set_cache


# -------- CONFIG --------
MAX_LINKS = 10
MAX_TOTAL_TEXT = 8000


# -------- Scrape + Clean --------
def scrape_and_clean(link):
    try:
        text = scrape_page(link)
        text = clean_text(text)
        return text[:1000]
    except Exception:
        return ""


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

Here is the report:
{previous}

Answer this follow-up question clearly and concisely:

{query}
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

    # -------- SEARCH --------
    links = search_company(company)
    if not links:
        return "No data sources found."

    links = list(set(links))[:MAX_LINKS]

    # -------- SCRAPE --------
    collected_chunks = []
    total_length = 0

    try:
        with ThreadPoolExecutor(max_workers=5) as executor:
            results = list(executor.map(scrape_and_clean, links))
    except Exception:
        results = []

    for text in results:
        if text:
            collected_chunks.append(text)
            total_length += len(text)

        if total_length >= MAX_TOTAL_TEXT:
            break

    if not collected_chunks:
        return "Failed to collect useful data."

    collected_text = "\n".join(collected_chunks)

    # -------- NEWS --------
    try:
        news_links = get_company_news(company)
    except Exception:
        news_links = []

    if news_links:
        news_text = "\nRecent News:\n"
        for n in news_links[:5]:
            news_text += f"- {n}\n"

        collected_text += "\n" + news_text

    # -------- PROMPT --------
    prompt = research_prompt(persona_prompt, company, collected_text)

    # -------- LLM --------
    result = ask_llm(prompt)

    # -------- STORE --------
    set_research(company, result)
    set_cache(cache_key, result)

    return result