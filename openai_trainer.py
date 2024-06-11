
import openai

# Set your OpenAI API key
openai.api_key = st.secrets["OpenAIAPI"]

# Define a function to perform sentiment analysis
def sentiment_analysis(text):
    # Use the OpenAI API to get the sentiment of the input text
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Analyze the sentiment of the following text:\n\n{text}\n\nSentiment:",
        max_tokens=1,
        n=1,
        stop=None,
        temperature=0.5,
    )

    # Extract the sentiment from the API response
    sentiment = response.choices[0].text.strip().lower()

    return sentiment

