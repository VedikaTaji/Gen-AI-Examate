# AQIExplainer Answer Evaluation

## Summary

- Total questions: 15
- Successful API calls: 7
- Failed API calls: 8
- API success rate: 46.67%
- Answer fact coverage: None
- Answer accuracy proxy: None
- Refusal accuracy: 71.43%
- Citation reference validity: 100%
- Average latency: 1.619 seconds

## Question-level results

| ID | API | Answer correct | Refusal correct | Citations valid | Latency (s) |
|---|---|---|---|---|---:|
| Q1 | True | None | True | True | 1.628 |
| Q2 | True | None | True | True | 1.396 |
| Q3 | True | None | True | True | 1.595 |
| Q4 | True | None | False | True | 1.842 |
| Q5 | True | None | False | True | 2.16 |
| Q6 | True | None | True | True | 1.622 |
| Q7 | False | None | False | False | 1.32 |
| Q8 | False | None | False | False | 1.287 |
| Q9 | False | None | False | False | 0.475 |
| Q10 | False | None | False | False | 0.439 |
| Q11 | True | None | True | True | 1.087 |
| Q12 | False | None | False | False | 0.434 |
| Q13 | False | None | False | False | 0.429 |
| Q14 | False | None | False | False | 0.452 |
| Q15 | False | None | False | False | 0.414 |

## Methodology and limitations

- Answer fact coverage is only calculated when expected_facts are provided.
- Exact phrase matching is a baseline, not semantic answer evaluation.
- Answer accuracy proxy uses a 50% expected-fact threshold.
- Refusal accuracy checks whether answerable questions receive an answer and unanswerable questions receive exactly 'I don't know'.
- Citation reference validity checks numbering against retrieved chunk count, not factual support.
- Citation coverage is the fraction of retrieved chunks referenced by the answer.
- API errors are counted separately from answer quality.
- Latency measures the complete answer_with_rag call.