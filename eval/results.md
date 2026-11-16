# AQIExplainer Retrieval Evaluation

## Configuration Comparison

| Configuration | Chunk Size | Overlap | Top-k | Keyword Hits | Hit Rate | Mean Similarity |
|---|---:|---:|---:|---:|---:|---:|
| Configuration A | 900 | 150 | 3 | 14/14 | 100.0% | 0.549 |
| Configuration B | 500 | 100 | 5 | 14/14 | 100.0% | 0.5191 |

## Winner

**Configuration A**

Winner selected by retrieval hit rate, with mean similarity as a tie-breaker.

## Q6 Abstention Check

Q6 is an unanswerable historical-data question. It is excluded from retrieval hit-rate calculations.
Verify that POST /ask returns exactly `I don't know`, with no citations and low confidence.

## Evaluation Method

Keyword hit rate measures whether at least one expected keyword appears in the retrieved chunks.
It is a simple retrieval relevance proxy, not a measure of answer correctness.
Mean similarity is the average similarity score of retrieved chunks for answerable questions.