import requests
from bs4 import BeautifulSoup
import re
import yfinance as yf


def search_for_stock_news_urls(ticker, source):
    """
    Fetch recent news URLs for a given stock ticker and source using yfinance.
    yfinance pulls news from Yahoo Finance's API, which aggregates articles
    from many sources (Bloomberg, Reuters, CNBC, Motley Fool, etc.).

    The 'source' parameter is used to filter articles by the provider name.
    """
    print(f"\n[DEBUG] Searching for news: {source} — {ticker} (via yfinance)")

    try:
        stock = yf.Ticker(ticker)
        news_items = stock.news
    except Exception as e:
        print(f"[ERROR] yfinance failed: {e}")
        return []

    print(f"[DEBUG] yfinance returned {len(news_items)} raw news items")

    # If source is a general term like "Yahoo Finance", "Bloomberg", etc.,
    # filter by the provider displayName
    raw_urls = []
    for item in news_items:
        content = item.get("content", {})
        provider = content.get("provider", {})
        provider_name = provider.get("displayName", "")
        title = content.get("title", "")
        canonical_url = content.get("canonicalUrl", {}).get("url", "")
        summary = content.get("summary", "")

        # Check if the provider matches the requested source (case-insensitive)
        if source.lower() in provider_name.lower():
            if canonical_url:
                raw_urls.append(canonical_url)
                print(f"   [{provider_name}] {title}")
                print(f"      → {canonical_url}")

    # If no articles matched the source filter, fall back to returning all
    # article URLs so we don't return empty-handed
    if not raw_urls:
        print(f"[DEBUG] No articles matched source '{source}'. Returning all available articles.")
        for item in news_items:
            content = item.get("content", {})
            provider = content.get("provider", {}).get("displayName", "Unknown")
            title = content.get("title", "")
            canonical_url = content.get("canonicalUrl", {}).get("url", "")
            if canonical_url:
                raw_urls.append(canonical_url)
                print(f"   [{provider}] {title}")
                print(f"      → {canonical_url}")

    print(f"[DEBUG] Final URL count: {len(raw_urls)}")
    return raw_urls


def strip_unwanted_urls(urls, excluded_list):
    print("\n[DEBUG] Filtering URLs...")
    excluded = set(excluded_list + ["google.com", "maps", "policies", "support"])

    clean = []
    for url in urls:
        if any(x in url for x in excluded):
            print(f"   [SKIP] {url}")
            continue
        print(f"   [KEEP] {url}")
        clean.append(url)

    print(f"[DEBUG] Final count: {len(clean)} URLs")
    return clean


def scrape_and_process(urls, word_limit=400):
    print("\n[DEBUG] Scraping articles...")
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
    articles = []

    for url in urls:
        print(f"\n[SCRAPE] {url}")
        try:
            r = requests.get(url, headers=headers, timeout=10)
            print(f"   Status: {r.status_code}")

            soup = BeautifulSoup(r.text, "html.parser")
            paragraphs = soup.find_all("p")
            print(f"   Found {len(paragraphs)} <p> tags")

            text = " ".join([p.get_text() for p in paragraphs])
            trimmed = " ".join(text.split()[:word_limit])

            print(f"   Extracted {len(trimmed.split())} words")
            articles.append(trimmed)

        except Exception as e:
            print(f"   [ERROR] {e}")
            articles.append(None)

    return articles


# test this app
if __name__ == "__main__":
    raw = search_for_stock_news_urls("TSLA", "Yahoo Finance")
    filtered = strip_unwanted_urls(raw, [])
    articles = scrape_and_process(filtered)

    print("\n=== FINAL ARTICLES ===")
    for i, a in enumerate(articles):
        print(f"\nArticle {i+1}:")
        if a:
            print(a[:500], "...")
        else:
            print("(None)")
