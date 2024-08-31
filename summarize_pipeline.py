# Use a pipeline as a high-level helper
from transformers import pipeline
#summarize_pipe = pipeline("summarization", model="facebook/bart-large-cnn")
# Load the model using PyTorch weights
summarize_pipe = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6", framework="pt")
