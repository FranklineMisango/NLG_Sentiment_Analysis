# Use a pipeline as a high-level helper
from transformers import pipeline
summarize_pipe = pipeline("summarization", model="facebook/bart-large-cnn")