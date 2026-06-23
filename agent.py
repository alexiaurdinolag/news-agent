import os
import requests
from datetime import datetime

NEWSAPI_KEY = os.environ["NEWSAPI_KEY"]

TOPICS = [
    "Latin America economy",
    "Mexico economy",
    "Brazil economy",
    "Argentina economy",
    "Colombia economy",
    "Chile economy",
    "US economy",
    "Federal Reserve",
    "US Latin America trade",
]

def fetch_news(topic):
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": topic,
        "sortBy": "publishedAt",
        "pageSize": 5,
        "language": "en",
        "apiKey": NEWSAPI_KEY,
    }
    res = requests.get(url, params=params)
    return res.json().get("articles", [])

def run():
    date = datetime.now().strftime("%B %d, %Y")
    print(f"\n{'='*50}")
    print(f"LATAM + US ECONOMIC BRIEFING — {date}")
    print(f"{'='*50}")

    for topic in TOPICS:
        print(f"\n>>> {topic.upper()}")
        articles = fetch_news(topic)
        if not articles:
            print("No articles found.")
            continue
        for a in articles:
            print(f"  - {a['title']}")
            print(f"    {a['source']['name']} | {a['publishedAt'][:10]}")

    print(f"\n{'='*50}\n")

if __name__ == "__main__":
    run()
