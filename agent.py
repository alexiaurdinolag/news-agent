import os
import requests
import google.generativeai as genai
from datetime import datetime

NEWSAPI_KEY = os.environ["NEWSAPI_KEY"]
GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

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
    articles = res.json().get("articles", [])
    return articles

def summarize(topic, articles):
    if not articles:
        return "No articles found."

    headlines = "\n".join([
        f"- {a['title']} ({a['source']['name']})"
        for a in articles if a.get("title")
    ])

    response = model.generate_content(f"""You are an economic analyst covering Latin America and the US.
Here are today's headlines about: {topic}

{headlines}

Give me:
1. The single most important story and why it matters
2. One sentence on the broader trend
Keep it concise and sharp.""")

    return response.text

def run():
    date = datetime.now().strftime("%B %d, %Y")
    print(f"\n{'='*50}")
    print(f"LATAM + US ECONOMIC BRIEFING — {date}")
    print(f"{'='*50}")

    for topic in TOPICS:
        print(f"\n>>> {topic.upper()}")
        articles = fetch_news(topic)
        summary = summarize(topic, articles)
        print(summary)

    print(f"\n{'='*50}\n")

if __name__ == "__main__":
    run()
