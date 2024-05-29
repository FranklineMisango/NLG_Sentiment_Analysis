import concurrent.futures
from trainer import summarizer, sentiment

def summarize_all_articles(articles):
    if articles is None:
        return {}  # Return an empty dictionary if articles is None

    summaries = {}
    for article in articles:
        # Perform summarization for each article and store the summary in the dictionary
        summary = summarizer(article, max_length=120, min_length=30, do_sample=False)
        if len(summary) > 0:
            summaries[article] = summary[0]['summary_text']
    
    return summaries

def perform_sentiment_analysis_on_single_summary(summary):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Submit a single task for executing sentiment analysis on the summary
        future = executor.submit(sentiment, summary)
        try:
            # Wait for the future to complete and get the result
            score = future.result()
            return score
        except Exception as e:
            print(f"Error occurred during sentiment analysis: {str(e)}")
            return None


'''
def main():
    user_ticker = input("Enter the ticker: ")
    source = input("Enter source: ")
    urls = search_for_stock_news_urls(user_ticker, source)
    excluded_list = ['maps', 'policies', 'preferences', 'support', 'accounts']
    cleaned_urls = strip_unwanted_urls(urls, excluded_list)
     # Printing the cleaned URLs as a list (formatted as a string)
    print("Printing URLS**")
    print("\n".join(cleaned_urls))
    print("\n")
    print("Printing final articles***")
    final_articles = scrape_and_process(cleaned_urls)
    print("\n".join(final_articles))
    print("\n*")
    print("Printing final Summaries***")
    final_summaries = summarize_all_articles(final_articles)
    print("\n".join(final_summaries))
    print("\n")
    print("Printing final scores**")
    final_scores = perform_sentiment_analysis(final_summaries, user_ticker)
    for ticker, score in final_scores.items():
        print(f"{ticker}: {score}")
if __name__ == "__main__":
    main()
'''