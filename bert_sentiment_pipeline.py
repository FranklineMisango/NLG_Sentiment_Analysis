# Use a pipeline as a high-level helper
from transformers import pipeline

bert_pipe = pipeline("text-classification", model="mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis")
def sentiment_bert_one(summary):
    try:
        score = bert_pipe(summary)
        return score
    except Exception as e:
        print(f"Error during sentiment analysis: {str(e)}")
        return None

  '''
    if add_selectbox == "BERT":
        ticker = st.text_input("Enter the stock/crypto ticker you want to monitor:")

        sources = ["Bloomberg", "Yahoo Finance", "Investopedia", "Google Finance"]
        source_choice = st.selectbox("Select the source you want to use:", sources)
        predict_button = st.button("Predict")

        if predict_button:
            st.header(f"Analysis for {ticker}, wait a few seconds....")
            excluded_list = ['maps', 'policies', 'preferences', 'support', 'accounts']
            raw_urls = {ticker: search_for_stock_news_urls(ticker, source_choice)}
            cleaned_urls = {ticker: strip_unwanted_urls(raw_urls[ticker], excluded_list)}
            articles = {ticker: scrape_and_process(cleaned_urls[ticker])}
            final_summaries = {ticker: summarize_all_articles(articles[ticker])}
            st.write(final_summaries)

            st.header("BERT Sentiment Analysis for the summaries below...")
            negative_summaries_count = 0

            for summary in final_summaries[ticker].values():
                st.write(summary)
                final_scores = sentiment_bert_one(summary)
                st.write(final_scores)
                negative_count = sum(1 for x in final_scores if x['label'] == 'NEGATIVE')
                if negative_count > 0:
                    negative_summaries_count += 1

            st.write(f"Total negative summaries post-sentiment analysis for {ticker}: {negative_summaries_count}")
            if negative_summaries_count > 5:
                st.warning(f"The model finds that stock {ticker} is not doing well currently. We recommend that you don't buy for short holding.")
            elif negative_summaries_count == 5:
                st.info(f"The model generates a neutral view on stock {ticker}, further research is needed: Bloomberg / Expedia refinement.")
            else:
                st.success(f"The model finds that stock {ticker} is good to buy for the short term. Contact our brokers to buy.")
'''
