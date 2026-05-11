import streamlit as st
from cleaner import search_for_stock_news_urls, strip_unwanted_urls, scrape_and_process
from openai_trainer import sentiment_analysis
from summaries import summarize_all_articles
from bert_sentiment_pipeline import sentiment_bert_one
from transformers import pipeline

st.set_page_config(page_title="Frankline & Co. Sentiment Analysis", layout="wide")

st.title("Frankline & Co. Ticker Sentiment Analysis")
st.success("Base Summarization done with BART, Sentiment done with selected pipelines")

pipeline_choice = st.sidebar.selectbox(
    "Which Pipeline would you like to use?",
    ("OpenAI", "BERT")
)

# Source options — "All" fetches from both NewsAPI + yfinance combined
source_options = [
    "All",
    "Yahoo Finance",
    "Bloomberg",
    "CNBC",
    "Reuters",
    "Motley Fool",
    "Investopedia",
    "Google Finance",
    "MarketWatch",
]


def main():
    ticker = st.text_input("Enter the stock/crypto/ETF ticker you want to monitor (e.g. TSLA, INTC, BTC-USD, SPY):")

    source_choice = st.selectbox("Select the source you want to use:", source_options)
    predict_button = st.button("Predict")

    if not predict_button or not ticker:
        return

    ticker = ticker.strip().upper()

    with st.spinner(f"Fetching & scraping news for {ticker}..."):
        excluded_list = ["maps", "policies", "preferences", "support", "accounts"]
        raw_urls = search_for_stock_news_urls(ticker, source_choice)
        cleaned_urls = strip_unwanted_urls(raw_urls, excluded_list)
        articles = scrape_and_process(cleaned_urls)

    # Show what we got
    valid_articles = [a for a in articles if a is not None]
    st.info(f"Found {len(raw_urls)} URLs, {len(cleaned_urls)} after filtering, {len(valid_articles)} successfully scraped")

    if not valid_articles:
        st.error("No articles could be scraped. Try a different ticker or source.")
        return

    # Show article previews in an expander
    with st.expander(f"View {len(valid_articles)} scraped articles"):
        for i, article_text in enumerate(valid_articles):
            st.markdown(f"**Article {i+1}** ({len(article_text.split())} words)")
            st.text_area(f"article_{i}", article_text, height=150, key=f"article_{i}", label_visibility="collapsed")
            st.divider()

    if pipeline_choice == "OpenAI":
        st.header(f"BART Summarization for {ticker}...")
        with st.spinner("Summarizing articles..."):
            final_summaries = summarize_all_articles(valid_articles)
            st.write(final_summaries)

        st.header("ChatGPT Sentiment Analysis")
        for summary in final_summaries.values():
            st.write(summary)
            with st.spinner("Analyzing sentiment..."):
                final_scores = sentiment_analysis(summary)
            st.success(final_scores)

    elif pipeline_choice == "BERT":
        st.header(f"BART Summarization for {ticker}...")
        with st.spinner("Summarizing articles..."):
            final_summaries = summarize_all_articles(valid_articles)
            st.write(final_summaries)

        st.header("BERT Sentiment Analysis")
        sentiment_pipeline = pipeline("sentiment-analysis", device=0)
        for summary in final_summaries.values():
            st.write(summary)
            with st.spinner("Analyzing sentiment..."):
                final_scores = sentiment_pipeline(summary)
            st.success(final_scores)


if __name__ == "__main__":
    main()
