"""
FastEmbed-based sentiment analysis for stock/crypto news articles.

Uses BGE-small-en-v1.5 embeddings with prototype centroids and softmax
normalization for zero-shot sentiment classification.
"""

import math
import os
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from fastembed import TextEmbedding

CENTROID_DIR = os.path.dirname(os.path.abspath(__file__))
POS_CENTROID_PATH = os.path.join(CENTROID_DIR, "pos_centroid.npy")
NEG_CENTROID_PATH = os.path.join(CENTROID_DIR, "neg_centroid.npy")
NEU_CENTROID_PATH = os.path.join(CENTROID_DIR, "neu_centroid.npy")

_embedder = None
_centroids = None


def _get_embedder():
    global _embedder
    if _embedder is None:
        _embedder = TextEmbedding(model_name="BAAI/bge-small-en-v1.5")
    return _embedder


def _get_centroids():
    global _centroids
    if _centroids is not None:
        return _centroids

    if all(os.path.exists(p) for p in [POS_CENTROID_PATH, NEG_CENTROID_PATH, NEU_CENTROID_PATH]):
        pos = np.load(POS_CENTROID_PATH)
        neg = np.load(NEG_CENTROID_PATH)
        neu = np.load(NEU_CENTROID_PATH)
        _centroids = {"positive": pos, "negative": neg, "neutral": neu}
        return _centroids

    positive_prototypes = [
        "Strong earnings beat with record revenue and expanding profit margins.",
        "Stock surging on positive analyst upgrades and strong demand outlook.",
        "Company launching innovative products driving massive adoption.",
        "Industry-leading performance with excellent free cash flow generation.",
        "Bullish outlook with raised guidance and accelerating market share.",
        "Breakthrough technology partnership expected to drive significant revenue.",
        "Exceptional quarter exceeds all expectations across every metric.",
        "Management executing flawlessly on growth strategy with momentum.",
        "Strong buy recommendations from analysts with high price targets.",
        "Record breaking sales figures and expanding customer base globally.",
        "Strategic acquisition expected to be immediately accretive to earnings.",
        "Company demonstrating resilient growth despite challenging environment.",
    ]
    negative_prototypes = [
        "Disappointing earnings miss with declining revenue and shrinking margins.",
        "Stock plummeting after catastrophic earnings report and lowered guidance.",
        "Company facing serious regulatory investigations and mounting lawsuits.",
        "Major product recall damaging brand reputation and consumer trust.",
        "Executive departures signal deep internal turmoil and leadership crisis.",
        "Debt downgrade amid concerns about ability to service obligations.",
        "Severe supply chain disruptions causing production halts and delays.",
        "Competitor gaining significant market share at company's expense.",
        "Fraud allegations triggering federal investigation and lawsuits.",
        "Layoffs and restructuring as company struggles with declining demand.",
        "Cash burn rate accelerating with no clear path to profitability.",
        "Analysts downgrade stock citing deteriorating fundamentals.",
    ]
    neutral_prototypes = [
        "Stock trading within expected range with no major catalyst today.",
        "Company announced routine quarterly dividend payment to shareholders.",
        "Industry conference scheduled for next week with panel discussions.",
        "Company filed standard regulatory paperwork with SEC on deadline.",
        "Trading volume in line with historical averages for the session.",
        "Board of directors announced regular annual meeting date.",
        "Company published updated corporate governance guidelines.",
        "Standard market making activity observed across the sector.",
        "Routine patent filing published by the patent office today.",
        "Company spokesperson declined to comment on market speculation.",
        "Analyst maintains hold rating with fair value estimate unchanged.",
        "Regular maintenance update released for company software products.",
    ]

    embedder = _get_embedder()
    pos_embs = list(embedder.embed(positive_prototypes))
    neg_embs = list(embedder.embed(negative_prototypes))
    neu_embs = list(embedder.embed(neutral_prototypes))

    pos_centroid = np.mean(pos_embs, axis=0)
    neg_centroid = np.mean(neg_embs, axis=0)
    neu_centroid = np.mean(neu_embs, axis=0)

    np.save(POS_CENTROID_PATH, pos_centroid)
    np.save(NEG_CENTROID_PATH, neg_centroid)
    np.save(NEU_CENTROID_PATH, neu_centroid)

    _centroids = {"positive": pos_centroid, "negative": neg_centroid, "neutral": neu_centroid}
    return _centroids


def analyze_sentiment(article_texts):
    single_mode = isinstance(article_texts, str)
    if single_mode:
        article_texts = [article_texts]

    embedder = _get_embedder()
    centroids = _get_centroids()
    embeddings = list(embedder.embed(article_texts))

    results = []
    for text, emb in zip(article_texts, embeddings):
        pos_sim = cosine_similarity([emb], [centroids["positive"]])[0][0]
        neg_sim = cosine_similarity([emb], [centroids["negative"]])[0][0]
        neu_sim = cosine_similarity([emb], [centroids["neutral"]])[0][0]

        e_pos, e_neg, e_neu = math.exp(pos_sim), math.exp(neg_sim), math.exp(neu_sim)
        total = e_pos + e_neg + e_neu
        softmax_pos = e_pos / total
        softmax_neg = e_neg / total
        softmax_neu = e_neu / total

        raw_diff = pos_sim - neg_sim
        polarity = math.tanh(raw_diff * 10)

        if softmax_pos > softmax_neg and softmax_pos > softmax_neu:
            sentiment = "POSITIVE"
            confidence = softmax_pos
        elif softmax_neg > softmax_neu:
            sentiment = "NEGATIVE"
            confidence = softmax_neg
        else:
            sentiment = "NEUTRAL"
            confidence = softmax_neu

        results.append({
            "sentiment": sentiment,
            "polarity": round(polarity, 4),
            "pos_score": round(softmax_pos, 4),
            "neg_score": round(softmax_neg, 4),
            "neu_score": round(softmax_neu, 4),
            "confidence": round(confidence, 4),
        })

    if single_mode:
        return results[0]

    polarities = [r["polarity"] for r in results]
    sentiments = [r["sentiment"] for r in results]
    avg_polarity = float(np.mean(polarities))
    bullish_pct = sentiments.count("POSITIVE") / len(sentiments) * 100
    bearish_pct = sentiments.count("NEGATIVE") / len(sentiments) * 100
    neutral_pct = sentiments.count("NEUTRAL") / len(sentiments) * 100

    if avg_polarity > 0.15:
        agg_sentiment = "BULLISH"
    elif avg_polarity < -0.15:
        agg_sentiment = "BEARISH"
    else:
        agg_sentiment = "NEUTRAL"

    return {
        "articles": results,
        "aggregate": {
            "sentiment": agg_sentiment,
            "avg_polarity": round(avg_polarity, 4),
            "bullish_pct": round(bullish_pct, 1),
            "bearish_pct": round(bearish_pct, 1),
            "neutral_pct": round(neutral_pct, 1),
            "article_count": len(results),
        },
    }


if __name__ == "__main__":
    from cleaner import search_for_stock_news_urls, strip_unwanted_urls, scrape_and_process

    raw = search_for_stock_news_urls("TSLA", "All")
    filtered = strip_unwanted_urls(raw, [])
    articles = scrape_and_process(filtered)
    valid = [a for a in articles if a]

    print(f"\nAnalyzing {len(valid)} articles...")
    result = analyze_sentiment(valid)

    print("\n=== PER-ARTICLE ===")
    for i, r in enumerate(result["articles"]):
        emoji = "\U0001f7e2" if r["sentiment"] == "POSITIVE" else "\U0001f534" if r["sentiment"] == "NEGATIVE" else "\U0001f7e1"
        print(f"{emoji} Article {i+1}: {r['sentiment']:8s} | polarity={r['polarity']:+.4f}")

    a = result["aggregate"]
    print(f"\n=== AGGREGATE ===")
    print(f"Overall: {a['sentiment']}")
    print(f"Avg polarity: {a['avg_polarity']:+.4f}")
    print(f"Distribution: {a['bullish_pct']:.0f}% bullish, {a['bearish_pct']:.0f}% bearish, {a['neutral_pct']:.0f}% neutral")
    print(f"Articles: {a['article_count']}")
