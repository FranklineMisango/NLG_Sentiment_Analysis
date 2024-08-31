# Use a pipeline as a high-level helper
#summarize_pipe = pipeline("summarization", model="facebook/bart-large-cnn")
# Load the model using PyTorch weights
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM

# Load the tokenizer
tokenizer = AutoTokenizer.from_pretrained("sshleifer/distilbart-cnn-12-6")

# Load the model using PyTorch weights
model = AutoModelForSeq2SeqLM.from_pretrained("sshleifer/distilbart-cnn-12-6")

# Create the pipeline
summarize_pipe = pipeline("summarization", model=model, tokenizer=tokenizer)
