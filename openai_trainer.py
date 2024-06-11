from openai import OpenAI
import streamlit as st
client = OpenAI(api_key=st.secrets["OpenAIAPI"])

# Set the OpenAI API key

# Define a function to perform sentiment analysis
def sentiment_analysis(text):
    # Use the OpenAI API to get the sentiment of the input text
    response = client.completions.create(
    prompt = f"Analyze the sentiment of the following text:\n\n{text}\n\nSentiment:",
    n = 1,
    stop = None,
    model = "gpt-3.5-turbo",
    max_tokens = 512,
    top_p =  1,
    temperature = 0.5,
    frequency_penalty = 0,
    presence_penalty = 0)

    # Extract the sentiment from the API response
    sentiment = response.choices[0].text.strip().lower()

    return sentiment
