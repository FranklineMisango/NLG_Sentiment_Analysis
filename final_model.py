#Unpack for future use
import pickle
from transformers import PegasusTokenizer, PegasusForConditionalGeneration
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline
import pickle

with open('trainer.pkl', 'rb') as f:
    model = pickle.load(f)


working_model = model
tokenizer = AutoTokenizer.from_pretrained(working_model, revision=model)
sentiment = pipeline('sentiment-analysis', model=model, tokenizer=tokenizer)


# Define the summarization pipeline
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")