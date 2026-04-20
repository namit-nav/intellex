import requests
from bs4 import BeautifulSoup


def scrape_page(url):

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code != 200:
            return ""

        soup = BeautifulSoup(response.text, "html.parser")

        paragraphs = soup.find_all("p")

        text = ""

        for p in paragraphs:
            content = p.get_text().strip()

            # Skip very short or useless lines
            if len(content) < 40:
                continue

            text += content + "\n"

            # Limit total size (important)
            if len(text) > 5000:
                break

        return text

    except Exception:
        return ""