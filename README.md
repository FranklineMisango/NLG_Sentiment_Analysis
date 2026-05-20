# Financial Sentiment Analysis: embedding-driven summaries and sentiment
This project evaluates methods for interpreting financial news and documents. The codebase contains both embedding-driven and model-based approaches; the primary production pipeline now uses sentence embeddings (extractive summarization and embedding-based sentiment scoring). BERT/BART models are retained for comparison and research experiments.

## Architecture
The updated processing pipeline is centered on sentence-level embeddings rather than relying primarily on BART for abstractive summaries. High-level flow:

- **Ingestion:** Articles are fetched by the ingestion layer (see `app.py` and `summarize_pipeline.py`). Sources supported in the repo include news APIs, RSS feeds, and local files (see `Stocks/` CSVs for examples).
- **Preprocessing:** Text cleaning and normalization happens in `cleaner.py` before embeddings are computed.
- **Embeddings:** Sentences and document chunks are converted to vector embeddings using the fast embedding pipeline (`sentiment_fastembed.py`) or external embeddings (OpenAI) as configured.
- **Summarization (extractive):** Summaries are produced by selecting representative sentences using embedding similarity to the document centroid or clustering (implemented in `summaries.py` and orchestrated by `summarize_pipeline.py`). This extractive, embedding-based approach is the default now; abstractive models (e.g., BART) are available for comparison but are no longer the dominant summarization method.
- **Sentiment Analysis:** Sentiment is scored by comparing article/sentence embeddings to precomputed centroids (`neg_centroid.npy`, `neu_centroid.npy`, `pos_centroid.npy`) and computing cosine similarity (see `sentiment_fastembed.py`). A BERT-based sentiment pipeline (`bert_sentiment_pipeline.py`) remains in the repo as an alternative baseline.
- **Serving & Experiments:** `app.py` provides a Streamlit UI for exploration and comparison. `openai_trainer.py` and other trainer scripts support experiments and fine-tuning when needed.

## Key files

- `app.py` — Streamlit app and entrypoint for interactive exploration.
- `summarize_pipeline.py` — Orchestrates ingestion → preprocessing → embedding → summary generation.
- `summaries.py` — Summary utilities and extractive selection logic.
- `cleaner.py` — Text cleaning and normalization.
- `sentiment_fastembed.py` — Embedding-based sentiment scoring and utilities.
- `bert_sentiment_pipeline.py` — BERT-based sentiment pipeline (baseline/comparison).
- `openai_trainer.py` — Trainer utilities for OpenAI-based experiments.
- `neg_centroid.npy`, `neu_centroid.npy`, `pos_centroid.npy` — Precomputed centroids used for fast embedding-based sentiment classification.

## Usage

1. Clone the repo and create a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the summarization pipeline (example):

```bash
python summarize_pipeline.py
```

4. Start the UI:

```bash
streamlit run app.py
```

Notes:
- The default summarization is extractive and embedding-based. Switch to abstractive model comparisons by running the BART/BERT scripts manually.
- If you want to use OpenAI embeddings instead of local embedding models, configure the appropriate API keys and trainer scripts.

## Limitations

- Embedding-based summaries are extractive (select existing sentences). For fully abstractive summaries, use the model-based scripts but expect different trade-offs in faithfulness vs. fluency.
- As with any automated sentiment pipeline, human review is recommended before making trading or investment decisions.

## Status
- Primary summarization: sentence-embedding extractive pipeline (default).
- Model baselines (BART/BERT/Llama) retained for comparison and research.

