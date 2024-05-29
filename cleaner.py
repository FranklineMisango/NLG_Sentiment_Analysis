import requests
from bs4 import BeautifulSoup
import re

def search_for_stock_news_urls(ticker, source):
    if source == "Bloomberg":
        search_url = f"https://www.google.com/search?q=bloomberg+{ticker}&tbm=nws"
    elif source == "Yahoo Finance":
        search_url = f"https://www.google.com/search?q=yahoo+finance+{ticker}&tbm=nws"
    elif source == "Investopedia":
        search_url = f"https://www.google.com/search?q=investopedia+{ticker}&tbm=nws"
    elif source == "Google Finance":
        search_url = f"https://www.google.com/search?q=google+finance++{ticker}&tbm=nws"
    else:
        return None

    r = requests.get(search_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    if source == "Bloomberg":
        atags = soup.find_all('a')
    elif source == "Yahoo Finance":
        atags = soup.find_all('a')
    elif source == "Investopedia":
        atags = soup.find_all('a')
    elif source == "Google Finance":
        atags = soup.find_all('a')
    else:
        return None

    hrefs = [link['href'] for link in atags]
    return hrefs

def strip_unwanted_urls(urls, excluded_list):
    excluded_list = ['maps', 'google','policies', 'preferences', 'support', 'accounts']
    if urls is None:
        return []
    final_val = []
    for url in urls:
        if 'https://' in url and not any(excluded_word in url for excluded_word in excluded_list):
            res = re.findall(r'(https?://\S+)', url)[0].split('&')[0]
            final_val.append(res)
    return list(set(final_val))

def scrape_and_process(urls, word_limit=400):
    articles = []
    for url in urls:
        try:
            # Common headers to mimic a browser request
            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/118.0'
            }
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            paragraphs = soup.find_all('p')
            
            # Extracting text while excluding specific boilerplate text
            text = [paragraph.text for paragraph in paragraphs if 'Bloomberg' not in paragraph.text]
            article_text = ' '.join(text)
            
            # Trimming the article to the desired word limit
            trimmed_article = ' '.join(article_text.split()[:word_limit])
            articles.append(trimmed_article)
            
            # Optional: Print the trimmed article for verification
            # print(trimmed_article)
        except Exception as e:
            print(f"Error occurred while scraping {url}: {str(e)}")
            articles.append(None)  # Consider if you want to keep track of failed URL scrapes
    return articles


#The code below is for tests
'''
def main():
    user_ticker = input("Enter the ticker: ")
    source = input("Enter source: ")
    urls = search_for_stock_news_urls(user_ticker, source)
    # Here, define your list of words to exclude from URLs
    excluded_list = ['maps', 'policies', 'preferences', 'support', 'accounts']
    cleaned_urls = strip_unwanted_urls(urls, excluded_list)
     # Printing the cleaned URLs as a list (formatted as a string)
    print("\n".join(cleaned_urls))
    scrape_and_process(cleaned_urls)
    
if __name__ == "__main__":
    main()
'''