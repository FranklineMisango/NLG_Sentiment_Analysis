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
