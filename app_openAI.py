
import streamlit as st
from cleaner import search_for_stock_news_urls, strip_unwanted_urls, scrape_and_process
from openai_trainer import sentiment_analysis
from summaries import summarize_all_articles

st.set_page_config(layout="wide")

def main():
    st.title("Frankline & Associates LLP. Self-rostering Ticker sentiment Analysis")
    st.success("Pipelining done to suit OpenAI_LLM")

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

        st.header("ChatGPT Sentiment Analysis for the summaries below...")
        for summary in final_summaries[ticker].values():
            st.write(summary)
            final_scores = sentiment_analysis(summary)
            st.write(final_scores)
            
if __name__ == '__main__':
    main()
