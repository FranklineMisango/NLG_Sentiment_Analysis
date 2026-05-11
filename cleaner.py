import yfinance as yf
from newsapi import NewsApiClient
from newspaper import Article as NewspaperArticle
from newspaper import ArticleException
import os
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()

# NewsAPI key
NEWSAPI_KEY = os.getenv("NEWS_API_KEY")



def search_for_stock_news_urls(ticker, source):
    """
    Fetch recent news URLs for a given ticker/symbol and source.
    Combines results from NewsAPI (up to 15) and yfinance (up to 10)
    for more articles, avoiding duplicates.

    Works for stocks, crypto (e.g. BTC-USD), ETFs (e.g. SPY), etc.

    The "source" parameter filters by provider/publication name.
    Use "All" to return everything.
    """
    print(f"\n[DEBUG] Searching for news: {source} -- {ticker}")

    seen_urls = set()
    all_urls = []

    # 1. NewsAPI
    newsapi_urls = _search_newsapi(ticker, source)
    for url in newsapi_urls:
        if url not in seen_urls:
            seen_urls.add(url)
            all_urls.append(url)

    # 2. yfinance (supplementary, different results)
    yf_urls = _search_yfinance(ticker, source)
    for url in yf_urls:
        if url not in seen_urls:
            seen_urls.add(url)
            all_urls.append(url)

    print(f"[DEBUG] Combined total: {len(all_urls)} unique URLs")
    return all_urls


def _search_newsapi(ticker, source, page_size=15):
    """Search news using NewsAPI."""
    print(f"[DEBUG] Using NewsAPI (ticker={ticker})")

    # Use the ticker itself in quotes for exact match, plus common terms
    query = f'"{ticker}" stock'
    # Also strip common yfinance suffixes like -USD for crypto
    base = ticker.split("-")[0]
    if base != ticker:
        query = f'"{base}" OR "{ticker}"'

    try:
        newsapi = NewsApiClient(api_key=NEWSAPI_KEY)
        results = newsapi.get_everything(
            q=query,
            language="en",
            sort_by="relevancy",
            page_size=page_size,
        )
    except Exception as e:
        print(f"[ERROR] NewsAPI call failed: {e}")
        return []

    articles_data = results.get("articles", [])
    total = results.get("totalResults", "?")
    print(f"[DEBUG] NewsAPI returned {len(articles_data)} articles (total={total})")

    if not articles_data:
        return []

    source_lower = source.lower().strip()
    return_all = source_lower in ("all", "all news", "general")
    raw_urls = []

    for article in articles_data:
        source_name = article.get("source", {}).get("name", "") or "Unknown"
        title = article.get("title", "") or ""
        url = article.get("url", "") or ""

        if not url or "consent.yahoo.com" in url:
            continue

        if return_all or source_lower in source_name.lower():
            raw_urls.append(url)
            print(f"   [NewsAPI][{source_name}] {title}")
            print(f"      -> {url}")

    if not raw_urls:
        print(f"[DEBUG] NewsAPI: no source match. Returning all.")
        for article in articles_data:
            source_name = article.get("source", {}).get("name", "") or "Unknown"
            title = article.get("title", "") or ""
            url = article.get("url", "") or ""
            if url and "consent.yahoo.com" not in url:
                raw_urls.append(url)
                print(f"   [NewsAPI][{source_name}] {title}")
                print(f"      -> {url}")

    print(f"[DEBUG] NewsAPI final URL count: {len(raw_urls)}")
    return raw_urls


def _search_yfinance(ticker, source):
    """Fetch news using yfinance (max 10 items)."""
    print(f"[DEBUG] Searching yfinance for: {ticker}")

    try:
        stock = yf.Ticker(ticker)
        news_items = stock.news
    except Exception as e:
        print(f"[ERROR] yfinance failed: {e}")
        return []

    print(f"[DEBUG] yfinance returned {len(news_items)} news items")

    source_lower = source.lower().strip()
    return_all = source_lower in ("all", "all news", "general")

    raw_urls = []
    for item in news_items:
        content = item.get("content", {})
        provider = content.get("provider", {})
        provider_name = provider.get("displayName", "")
        title = content.get("title", "")
        canonical_url = content.get("canonicalUrl", {}).get("url", "")

        if not canonical_url:
            continue

        if return_all or source_lower in provider_name.lower():
            raw_urls.append(canonical_url)
            print(f"   [yfinance][{provider_name}] {title}")
            print(f"      -> {canonical_url}")

    if not raw_urls:
        print(f"[DEBUG] yfinance: no source match. Returning all.")
        for item in news_items:
            content = item.get("content", {})
            provider = content.get("provider", {}).get("displayName", "Unknown")
            title = content.get("title", "")
            canonical_url = content.get("canonicalUrl", {}).get("url", "")
            if canonical_url:
                raw_urls.append(canonical_url)
                print(f"   [yfinance][{provider}] {title}")
                print(f"      -> {canonical_url}")

    print(f"[DEBUG] yfinance final URL count: {len(raw_urls)}")
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


def scrape_and_process(urls, word_limit=None):
    """
    Scrape article text from a list of URLs using newspaper3k.
    newspaper3k handles JS-heavy sites, extracts clean body text,
    and strips out ads/navigation/menus automatically.
    """
    print("\n[DEBUG] Scraping articles with newspaper3k...")
    articles = []

    for url in urls:
        print(f"\n[SCRAPE] {url}")
        article = NewspaperArticle(url)
        try:
            article.download()
            article.parse()

            text = article.text
            if not text:
                print("   [WARNING] No text extracted")
                articles.append(None)
                continue

            if word_limit is not None:
                text = " ".join(text.split()[:word_limit])

            print(f"   Title: {article.title[:100]}")
            word_count = len(text.split())
            print(f"   Extracted {word_count} words")
            articles.append(text)

        except ArticleException as e:
            print(f"   [ERROR] newspaper3k failed: {e}")
            articles.append(None)
        except Exception as e:
            print(f"   [ERROR] {e}")
            articles.append(None)

    return articles


'''
if __name__ == "__main__":
    raw = search_for_stock_news_urls("SNDK", "All")
    filtered = strip_unwanted_urls(raw, [])
    articles = scrape_and_process(filtered)

    print("\n=== FINAL ARTICLES ===")
    for i, a in enumerate(articles):
        print(f"\n{'='*60}")
        print(f"Article {i+1}:")
        print(f"{'='*60}")
        if a:
            print(a)
        else:
            print("(None)")
'''
