from research.search import search_company
from research.web_scraper import scrape_page
from research.text_cleaner import clean_text
from research.news_collector import get_company_news
from agents.persona_manager import get_persona_prompt
from core.llm import ask_llm
from core.prompts import research_prompt
from concurrent.futures import ThreadPoolExecutor
from core.memory import set_research, is_same_company, clear_chat_memory
from core.cache import get_cache, set_cache


# -------- CONFIG --------
MAX_LINKS = 10
MAX_TOTAL_TEXT = 8000


# -------- Scrape + Clean --------
def scrape_and_clean(link):
    try:
        page_text = scrape_page(link)
        page_text = clean_text(page_text)
        return page_text[:1000]
    except Exception:
        return ""


# -------- Main Research --------
def research_company(company, persona="research_assistant"):

    if not company:
        return "❌ Please provide a company name."

    company_clean = company.lower().strip()
    persona_clean = persona.lower().strip()

    cache_key = f"{company_clean}_{persona_clean}"
    cached_result = get_cache(cache_key)

    if cached_result:
        print("⚡ Using cached result")
        return cached_result

    # -------- Reset chat if new company --------
    if not is_same_company(company):
        clear_chat_memory()

    print("🔎 Generating research report...")

    # -------- Persona --------
    persona_prompt = get_persona_prompt(persona)

    # -------- Search --------
    links = search_company(company)
    links = list(set(links))[:MAX_LINKS]

    if not links:
        return "❌ No data sources found."

    # -------- Parallel Scraping --------
    collected_chunks = []

    with ThreadPoolExecutor(max_workers=5) as executor:
        results = executor.map(scrape_and_clean, links)

    total_length = 0

    for text in results:
        if text:
            collected_chunks.append(text)
            total_length += len(text)

        if total_length > MAX_TOTAL_TEXT:
            break

    collected_text = "\n".join(collected_chunks)

    if not collected_text:
        return "❌ Failed to collect useful data."

    # -------- Add News --------
    news_links = get_company_news(company)

    news_text = "\nRecent News Sources:\n"
    for n in news_links[:5]:
        news_text += f"- {n}\n"

    collected_text += "\n" + news_text

    # -------- Prompt --------
    prompt = research_prompt(persona_prompt, company, collected_text)

    # -------- LLM --------
    result = ask_llm(prompt)

    # -------- Store --------
    set_research(company, result)
    set_cache(cache_key, result)

    return result


# -------- CLI Test --------
if __name__ == "__main__":

    company = input("Enter company name: ")
    persona = input("Choose persona (research_assistant / market_analyst / sales_strategist): ")

    report = research_company(company, persona)

    print("\nResearch Report:\n")
    print(report)