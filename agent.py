# ─────────────────────────────────────────────────────────────
#  FINANCIAL NEWS ANALYST AGENT
#  Course: Financial Modeling | American University
#  Author: Abd Alghani Rahmoun
#  Model: Llama-3.3-70b via Groq (free)
# ─────────────────────────────────────────────────────────────

import os
import requests
from groq import Groq
from dotenv import load_dotenv

# ── Load API keys ─────────────────────────────────────────────
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
NEWS_API_KEY = os.getenv("NEWS_API_KEY")


# ── TOOL 1: Fetch live financial headlines ────────────────────
def fetch_headlines():
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": "finance OR stock market OR Federal Reserve OR banking OR inflation",
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 5,
        "apiKey": NEWS_API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()

    if data.get("status") != "ok":
        return []

    articles = []
    for article in data["articles"]:
        articles.append({
            "title":       article["title"],
            "description": article.get("description", "No description available."),
            "source":      article["source"]["name"],
            "url":         article["url"]
        })
    return articles


# ── TOOL 2: Analyze each headline with Llama via Groq ─────────
def analyze_headline(title, description):
    prompt = f"""You are a financial analyst. Analyze this news headline and description.

Headline: {title}
Description: {description}

Respond in exactly this format with no extra text:
SUMMARY: [2 sentence plain-English summary of what happened and why it matters to investors]
SENTIMENT: [BULLISH / BEARISH / NEUTRAL]
REASON: [1 sentence explaining why you chose that sentiment]"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200,
        temperature=0.3
    )
    return response.choices[0].message.content.strip()


# ── TOOL 3: Parse the AI response into a clean dictionary ─────
def parse_analysis(analysis):
    parsed = {}
    for line in analysis.split("\n"):
        if ":" in line:
            key, val = line.split(":", 1)
            parsed[key.strip()] = val.strip()
    return parsed


# ── MAIN: Run the full agent and return results ───────────────
def run_agent():
    articles = fetch_headlines()

    if not articles:
        return []

    results = []
    for article in articles:
        analysis = analyze_headline(article["title"], article["description"])
        parsed   = parse_analysis(analysis)

        results.append({
            "title":     article["title"],
            "source":    article["source"],
            "url":       article["url"],
            "sentiment": parsed.get("SENTIMENT", "NEUTRAL").upper(),
            "summary":   parsed.get("SUMMARY",   "N/A"),
            "reason":    parsed.get("REASON",     "N/A")
        })

    return results