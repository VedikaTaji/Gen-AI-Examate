# How Large Language Models (LLMs) Work

## 1. What is an LLM?

A Large Language Model (LLM) is an Artificial Intelligence model trained on a very large amount of text. It learns patterns in language and uses those patterns to understand prompts and generate human-like responses.

Examples of LLMs include GPT, Gemini, and Llama.

## 2. How does an LLM work?

An LLM works through the following steps:

1. **Input:** The user enters a question or instruction.
2. **Tokenization:** The text is divided into smaller pieces called tokens. A token can be a word, part of a word, or punctuation.
3. **Embedding:** Tokens are converted into numerical representations that the model can process.
4. **Transformer:** The Transformer architecture uses attention mechanisms to understand relationships between tokens and their context.
5. **Prediction:** The model calculates which token is likely to come next.
6. **Output:** It generates tokens one after another to produce a response.

## 3. Diagram: LLM Working Process

```text
       User Prompt
            |
            v
       Tokenization
            |
            v
        Embeddings
            |
            v
    Transformer Model
     (Self-Attention)
            |
            v
   Next-Token Prediction
            |
            v
     Generated Response
```

## 4. What is a Transformer?

A Transformer is a deep learning architecture widely used in modern LLMs.

Its important component is **self-attention**. Self-attention helps the model identify which words or tokens are important in relation to other tokens in the input.

For example, in the sentence "The air quality in Pune is poor because pollution levels are high", the model can use the context of the sentence to understand the relationship between air quality, Pune, and pollution.

## 5. How are LLMs trained?

LLM development commonly involves these stages:

- **Pre-training:** The model learns language patterns from a large text dataset, often by predicting missing or next tokens.
- **Fine-tuning:** The model is further trained on selected examples to improve its performance on particular tasks.
- **Alignment:** Techniques such as human feedback can help make responses more useful and appropriate.

## 6. LLMs and AQIExplainer

AQIExplainer currently uses a structured AQI dataset containing city, AQI value, AQI category, prominent pollutant, and reporting-station information.

The project currently uses:

- Python for application logic.
- FastAPI for API endpoints.
- Pandas for data analysis.
- TF-IDF for converting text into numerical feature vectors.
- Cosine similarity for ranking matching AQI records.

**Current limitation:** AQIExplainer does not currently use an LLM. Its `/questions` endpoint uses predefined rules and smart search to answer questions from the available records.

An LLM could be integrated in a future version to generate more natural explanations, but it would still need reliable AQI data to support factual answers.

## 7. Limitations of LLMs

- They can generate incorrect or misleading information.
- Their answers depend on the information and context available to them.
- They may not know current events or live data without an external data source.
- Their responses should be verified for important decisions.

## 8. Conclusion

LLMs combine large-scale language training with Transformer-based architectures to generate text. They are useful for conversational applications, summarization, question answering, and many other language tasks. However, reliable data and verification are still important for building trustworthy AI applications.