from transformers import PegasusTokenizer, PegasusForConditionalGeneration
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline

#Importing the BERT sentiment analysis model

model_name = "distilbert-base-uncased-finetuned-sst-2-english"
model_revision = "af0f99b"
model = AutoModelForSequenceClassification.from_pretrained(model_name, revision=model_revision)
tokenizer = AutoTokenizer.from_pretrained(model_name, revision=model_revision)
sentiment = pipeline('sentiment-analysis', model=model, tokenizer=tokenizer)


# Define the summarization pipeline
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

