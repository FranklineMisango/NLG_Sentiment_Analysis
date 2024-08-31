
import streamlit as st
from cleaner import search_for_stock_news_urls, strip_unwanted_urls, scrape_and_process
from openai_trainer import sentiment_analysis
from summaries import summarize_all_articles
#from bert_sentiment_pipeline import sentiment_bert_one

st.set_page_config(layout="wide")


# Using object notation
st.title("Frankline & Co. Self-rostering Ticker sentiment Analysis")
st.success("Base Summarization done with BART, Sentiment done with selected pipelines")

add_selectbox = st.sidebar.selectbox(
    "Which Pipeline would you like to use?",
    ("OpenAI")) # Add BERT if you need more computation power
def main():
    if add_selectbox == "OpenAI":
        ticker = st.text_input("Enter the stock/crypto ticker you want to monitor:")

        sources = ["Bloomberg", "Yahoo Finance", "Investopedia", "Google Finance"]
        source_choice = st.selectbox("Select the source you want to use:", sources)
        predict_button = st.button("Predict")

        if predict_button:
            st.header(f"BART Summarization for {ticker}, wait a few moments....")
            excluded_list = ['maps', 'policies', 'preferences', 'support', 'accounts']
            raw_urls = {ticker: search_for_stock_news_urls(ticker, source_choice)}
            cleaned_urls = {ticker: strip_unwanted_urls(raw_urls[ticker], excluded_list)}
            articles = {ticker: scrape_and_process(cleaned_urls[ticker])}
            final_summaries = {ticker: summarize_all_articles(articles[ticker])}
            st.write(final_summaries)

            st.header("ChatGPT Did the sentiment Analysis for the summaries below.....")
            for summary in final_summaries[ticker].values():
                st.write(summary)
                final_scores = sentiment_analysis(summary)
                st.success(final_scores)

  
if __name__ == '__main__':
    main()
