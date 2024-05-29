import streamlit as st
st.set_page_config(layout="wide")
import cleaner
import summaries
def main():
    st.title("Frankline & Associates LLP. Self-rostering Ticker sentiment Analysis")
    st.success("Pipelining done to suit Google's BERT & Meta BART Summarizer")

    #st.image('images/cover.png')

    ticker = st.text_input("Enter the stock/crypto ticker you want to monitor:")

    sources = ["Bloomberg", "Yahoo Finance", "Investopedia", "Google Finance"]
    source_choice = st.selectbox("Select the source you want to use:", sources)
    predict_button = st.button("Predict")

    stop_words = [
    'Ourengineersareworkingquicklytoresolvetheissue. Thankyouforyourpatience. Back to Mail Online home. back to the page you came from.',
    ' PleasemakesureyourbrowsersupportsJavaScriptandcookiesandthatyouarenotblockingthemfromloading. Tocontinue,pleaseclicktheboxbelowtoletusknowyou renotarobot.'
    
    ]
    if predict_button:
        st.header(f"Analysis for {ticker}, wait a few seconds....")
        excluded_list = ['maps', 'policies', 'preferences', 'support', 'accounts']
        raw_urls = {ticker: cleaner.search_for_stock_news_urls(ticker, source_choice)}
        cleaned_urls = {ticker: cleaner.strip_unwanted_urls(raw_urls[ticker], excluded_list)}
        articles = {ticker: cleaner.scrape_and_process(cleaned_urls[ticker])}
        final_summaries = {ticker: summaries.summarize_all_articles(articles[ticker])}
        st.write(final_summaries)

        #The Feature to print the summaries separately
        st.header("BERT Sentiment Analysis for the summaries below...")
        for i in final_summaries:
            st.success("The score of the sentiment from summaries above below ")
            final_ones = []
            final_values = final_summaries[i].values()
            for i in final_values:
                st.write(i)
                final_scores = summaries.perform_sentiment_analysis_on_single_summary(i)
                st.write(final_scores)
                negative_count = sum(1 for x in final_scores if x ['label'] == 'NEGATIVE')
                if negative_count:
                    final_ones.append(negative_count)

        st.write(f"Total negative summaries post-sentiment analysis for {ticker} : {final_ones.count(1)}")
        final_ones_pass = final_ones.count(1)
        if final_ones_pass > 5:
            st.warning(f"The model finds that stock {ticker} is not doing well currently. We recommend that you don't buy for short holding.")
        elif final_ones_pass == 5:
            st.info(f"The model generates a neutral view on stock {ticker}, further research is needed: Bloomberg / Expedia refinement.")
        elif final_ones_pass < 5:
            st.success(f"The model finds that stock {ticker} is good to buy for the short term. Contact our brokers to buy.")
if __name__ == '__main__':
    main()