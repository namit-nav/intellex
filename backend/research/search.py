import requests
from bs4 import BeautifulSoup
import urllib.parse


def search_company(company):

    query = urllib.parse.quote(company + " company overview products revenue competitors")

    url = f"https://duckduckgo.com/html/?q={query}"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    links = []

    try:
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code != 200:
            return []

        soup = BeautifulSoup(response.text, "html.parser")

        results = soup.find_all("a", class_="result__a")

        for r in results:
            link = r.get("href")

            if not link:
                continue

            if "uddg=" in link:
                real_url = link.split("uddg=")[1]
                real_url = urllib.parse.unquote(real_url)

                # Remove tracking junk (&rut=...)
                real_url = real_url.split("&")[0]

                links.append(real_url)

        # Remove duplicates
        links = list(set(links))

        return links[:4]

    except Exception:
        return []