import openai
import streamlit as st

# Set the OpenAI API key
openai.api_key = st.secrets["OpenAIAPI"]

# Define a function to perform sentiment analysis
def sentiment_analysis(text):
    # Use the OpenAI API to get the sentiment of the input text
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Analyze the sentiment of the given text and return a detailed response (positive, negative, or neutral) with a brief explanation."},
            {"role": "user", "content": text}
        ],
        max_tokens=256,  # Adjust to suit your needs
        n=1,
        stop=None,
        temperature=0.5,
        frequency_penalty=0,
        presence_penalty=0
    )

    # Extract the sentiment from the API response
    sentiment_response = response.choices[0].message.content.strip()

    return sentiment_response
