import requests
from bs4 import BeautifulSoup
import urllib.parse


def get_company_news(company):

    query = company + " news"

    url = f"https://duckduckgo.com/html/?q={query}"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, "html.parser")

    news_links = []

    results = soup.find_all("a", class_="result__a")

    for r in results:

        link = r.get("href")

        if "uddg=" in link:
            real_url = link.split("uddg=")[1]
            real_url = urllib.parse.unquote(real_url)

            news_links.append(real_url)

    return news_links[:5]


if __name__ == "__main__":

    news = get_company_news("Tesla")

    for n in news:
        print(n)