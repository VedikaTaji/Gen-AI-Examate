# AQIExplainer Advanced Retrieval Evaluation

## Configuration Comparison

| Configuration | Chunk | Overlap | Top-k | Keyword Hit Rate | Precision@K | Recall@K | MRR | Mean Similarity |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Configuration A | 900 | 150 | 3 | 100.0% | 0.9286 | 0.75 | 0.9524 | 0.549 |
| Configuration B | 500 | 100 | 5 | 100.0% | 0.8571 | 0.7738 | 0.9464 | 0.5191 |

## Winner

**Configuration B**

Winner selected using Recall@K, Precision@K, and MRR.

## Evaluation Method and Limitations

- Keyword hit rate checks whether at least one expected evidence group appears in retrieved text.
- Precision@K measures the proportion of retrieved chunks matching at least one expected evidence group.
- Recall@K measures the proportion of expected evidence groups found in retrieved chunks.
- MRR measures the reciprocal rank of the first chunk matching an expected evidence group.
- Mean similarity is a retrieval-distance diagnostic, not proof of relevance.
- These metrics use keyword matching as a relevance proxy. They are not human-verified semantic relevance or answer correctness.

## Unanswerable Questions

Unanswerable questions are excluded from retrieval quality averages.
Their answer refusal behavior must be evaluated separately.

## Detailed Results

### Configuration A

| ID | Keyword Hit | Precision@K | Recall@K | MRR |
|---|---|---:|---:|---:|
| Q1 | True | 1.0 | 1.0 | 1.0 |
| Q2 | True | 1.0 | 1.0 | 1.0 |
| Q3 | True | 1.0 | 0.5 | 1.0 |
| Q4 | True | 1.0 | 0.5 | 1.0 |
| Q5 | True | 0.3333 | 0.5 | 0.3333 |
| Q6 | None | None | None | None |
| Q7 | True | 1.0 | 1.0 | 1.0 |
| Q8 | True | 0.6667 | 1.0 | 1.0 |
| Q9 | True | 1.0 | 1.0 | 1.0 |
| Q10 | True | 1.0 | 0.5 | 1.0 |
| Q11 | True | 1.0 | 0.5 | 1.0 |
| Q12 | True | 1.0 | 1.0 | 1.0 |
| Q13 | True | 1.0 | 1.0 | 1.0 |
| Q14 | True | 1.0 | 0.3333 | 1.0 |
| Q15 | True | 1.0 | 0.6667 | 1.0 |

### Configuration B

| ID | Keyword Hit | Precision@K | Recall@K | MRR |
|---|---|---:|---:|---:|
| Q1 | True | 1.0 | 1.0 | 1.0 |
| Q2 | True | 0.8 | 1.0 | 1.0 |
| Q3 | True | 1.0 | 0.5 | 1.0 |
| Q4 | True | 1.0 | 0.5 | 1.0 |
| Q5 | True | 0.2 | 0.5 | 0.25 |
| Q6 | None | None | None | None |
| Q7 | True | 0.8 | 1.0 | 1.0 |
| Q8 | True | 0.8 | 1.0 | 1.0 |
| Q9 | True | 0.6 | 1.0 | 1.0 |
| Q10 | True | 1.0 | 0.5 | 1.0 |
| Q11 | True | 1.0 | 0.5 | 1.0 |
| Q12 | True | 1.0 | 1.0 | 1.0 |
| Q13 | True | 0.8 | 1.0 | 1.0 |
| Q14 | True | 1.0 | 0.6667 | 1.0 |
| Q15 | True | 1.0 | 0.6667 | 1.0 |
