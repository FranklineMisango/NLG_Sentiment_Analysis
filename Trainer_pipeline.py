# Use a pipeline as a high-level helper
from transformers import pipeline
pipe = pipeline("summarization", model="facebook/bart-large-cnn")

