import concurrent.futures
from summarize_pipeline import summarize_pipe

def summarize_article(article):
    try: 
        summary = summarize_pipe(article, max_length=120, min_length=30, do_sample=False) #Testing high level pipelines
        if summary and len(summary) > 0:
            return summary[0]['summary_text']
        return None
    except Exception as e:
        print(f"Error summarizing article: {str(e)}")
        return None

def summarize_all_articles(articles):
    if not articles:
        return {}  # Return an empty dictionary if articles is None or empty

    summaries = {}
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_article = {executor.submit(summarize_article, article): article for article in articles}
        for future in concurrent.futures.as_completed(future_to_article):
            article = future_to_article[future]
            try:
                summary = future.result()
                if summary:
                    summaries[article] = summary
            except Exception as e:
                print(f"Error processing article: {article}, {str(e)}")

    return summaries