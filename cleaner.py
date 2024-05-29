import requests
from bs4 import BeautifulSoup
import re

def search_for_stock_news_urls(ticker, source):
    search_urls = {
        "Bloomberg": f"https://www.google.com/search?q=bloomberg+{ticker}&tbm=nws",
        "Yahoo Finance": f"https://www.google.com/search?q=yahoo+finance+{ticker}&tbm=nws",
        "Investopedia": f"https://www.google.com/search?q=investopedia+{ticker}&tbm=nws",
        "Google Finance": f"https://www.google.com/search?q=google+finance+{ticker}&tbm=nws"
    }
    
    search_url = search_urls.get(source)
    if not search_url:
        return []

    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    atags = soup.find_all('a')
    hrefs = [link.get('href', '') for link in atags]

    return hrefs

def strip_unwanted_urls(urls, excluded_list):
    if not urls:
        return []

    excluded_set = set(excluded_list + ['maps', 'google', 'policies', 'preferences', 'support', 'accounts'])
    final_urls = []

    for url in urls:
        if 'https://' in url and not any(excluded_word in url for excluded_word in excluded_set):
            match = re.search(r'(https?://\S+)', url)
            if match:
                cleaned_url = match.group().split('&')[0]
                final_urls.append(cleaned_url)

    return list(set(final_urls))

def scrape_and_process(urls, word_limit=400):
    articles = []
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/118.0'}

    for url in urls:
        try:
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            paragraphs = soup.find_all('p')
            text = [p.get_text() for p in paragraphs if 'Bloomberg' not in p.get_text()]
            article_text = ' '.join(text)
            trimmed_article = ' '.join(article_text.split()[:word_limit])
            articles.append(trimmed_article)
        except Exception as e:
            print(f"Error occurred while scraping {url}: {e}")
            articles.append(None)  # This can be useful for debugging which URLs failed

    return articles
