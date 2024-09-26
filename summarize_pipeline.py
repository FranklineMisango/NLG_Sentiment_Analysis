# Use a pipeline as a high-level helper


# Load the model using PyTorch weights
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM

# Create the pipeline with GPU support
summarize_pipe = pipeline("summarization", model="facebook/bart-large-cnn")
