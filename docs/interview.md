# AQIExplainer — Interview Preparation

## 1. My 60-Second Project Pitch

AQIExplainer is a Generative AI-based Air Quality Analysis System that helps users understand air quality information across cities in Maharashtra.

The main problem I wanted to solve was that AQI bulletins contain a lot of technical information, and it is not always easy for ordinary users to understand AQI values, pollutant levels and their health implications.

I developed the application using Python, FastAPI and Streamlit. It combines document processing, semantic search, ChromaDB and Retrieval-Augmented Generation to retrieve relevant AQI information and generate context-grounded answers using Groq and Gemini.

I also implemented a CPCB-based AQI calculator that calculates pollutant sub-indices using breakpoint interpolation rather than allowing an LLM to guess numerical results. For more complex requests, I integrated an agent workflow using LangGraph with human approval.

The system also includes automated tests, input validation, prompt-injection screening, caching and request monitoring.

The most challenging part was extracting accurate structured data from complex multi-page CPCB PDF tables. This project helped me understand how to combine traditional data processing with Generative AI while maintaining numerical accuracy and source traceability.

## 2. Ten Likely Interview Questions and Answers

### Q1. What problem does AQIExplainer solve?

AQI information is publicly available, but users may find it difficult to interpret AQI values, pollutant concentrations and technical reports.

AQIExplainer organizes AQI information and provides:
- City-wise AQI information.
- Pollutant and monitoring information.
- Semantic document search.
- AI-generated explanations grounded in retrieved documents.
- CPCB-based pollutant sub-index calculations.

The goal is to make air quality information easier to access and understand.

### Q2. Explain the architecture of your project.

The project has a modular architecture:

1. Streamlit provides the user interface.
2. FastAPI handles API requests.
3. Input validation and guardrails check incoming requests.
4. The RAG pipeline retrieves relevant document chunks.
5. ChromaDB stores and retrieves document embeddings.
6. Groq or Gemini generates a response using retrieved context.
7. The AQI calculator handles numerical pollutant calculations.
8. LangGraph supports conditional routing and human approval.
9. The response is returned to the Streamlit interface.

The application also tracks request latency and token usage for the `/ask` endpoint.

### Q3. What was the hardest technical problem you faced?

One of the hardest problems was extracting structured data from CPCB PDF bulletins.

Each bulletin contained approximately 14 pages of tables. Extracting these tables correctly was difficult because:

- City names sometimes wrapped across multiple lines.
- Table rows could break across page boundaries.
- Pollutant names appeared in inconsistent formats, such as `PM 2.5 , PM 10`.
- Simple text extraction could lose the relationship between a city and its pollutant values.

I had to think about the extraction process as a structured-data problem rather than simply extracting plain text.

Another important challenge was numerical correctness. AQI values must be calculated using CPCB breakpoint interpolation. I did not want an LLM to invent or estimate AQI values.

### Q4. Why did you use RAG instead of sending the entire PDF to an LLM?

Sending an entire PDF directly to an LLM can increase token usage and may introduce irrelevant context.

RAG solves this by:

1. Extracting document text.
2. Splitting it into smaller overlapping chunks.
3. Generating embeddings.
4. Storing embeddings in ChromaDB.
5. Retrieving relevant chunks for a user's question.
6. Passing the retrieved context to the LLM.

This makes responses more context-specific and supports source-based citations.

### Q5. How does your AQI calculator work?

The calculator uses pollutant-specific CPCB breakpoints.

For each pollutant, it identifies the concentration interval containing the measured value and applies linear interpolation between the corresponding AQI breakpoints.

The general interpolation formula is:

`Ip = [(IHi - ILo) / (BPHi - BPLo)] × (Cp - BPLo) + ILo`

Where:

- `Ip` = pollutant sub-index.
- `Cp` = measured pollutant concentration.
- `BPHi` and `BPLo` = upper and lower concentration breakpoints.
- `IHi` and `ILo` = corresponding AQI breakpoints.

The overall AQI is determined from the highest pollutant sub-index, and that pollutant is identified as the dominant pollutant.

This numerical calculation is handled by Python, not guessed by the LLM.

### Q6. Why is the city AQI calculated as an average of monitoring stations a limitation?

A city can have multiple monitoring stations, and pollution levels may vary across locations.

Taking a simple arithmetic average of station AQI values is a simplification. It treats each station equally and does not fully represent differences in population exposure, geographic distribution or monitoring coverage.

CPCB itself flags this kind of city-level aggregation as a simplification.

Therefore, a city average should be treated as a summary indicator, not as an exact representation of the air quality experienced by every person in the city.

### Q7. How do you reduce hallucinations in your project?

I use multiple approaches:

- RAG retrieves relevant document context before answer generation.
- The system provides source-based citations.
- The prompt instructs the LLM to use the supplied context.
- The system can abstain when information is unavailable.
- Numerical AQI calculations are performed by deterministic Python functions.
- Input guardrails screen common prompt-injection attempts.

These measures reduce hallucination risk, although they do not guarantee that every generated answer is correct.

### Q8. How did you evaluate the retrieval system?

I created a 15-question AQI evaluation dataset and compared two retrieval configurations.

Configuration A:
- Chunk size: 900.
- Overlap: 150.
- Top-k: 3.

Configuration B:
- Chunk size: 500.
- Overlap: 100.
- Top-k: 5.

I evaluated keyword hit rate, Precision@K, Recall@K, Mean Reciprocal Rank and mean similarity.

Configuration A achieved:
- Keyword hit rate: 100%.
- Precision@K: 0.9286.
- Recall@K: 0.7500.
- MRR: 0.9524.
- Mean similarity: 0.5490.

Configuration B achieved:
- Keyword hit rate: 100%.
- Precision@K: 0.8571.
- Recall@K: 0.7738.
- MRR: 0.9464.
- Mean similarity: 0.5191.

I selected Configuration A because it performed better on precision-oriented metrics and MRR. These are retrieval metrics, not proof of factual answer accuracy.

### Q9. Why did you use LangGraph and human-in-the-loop approval?

I used LangGraph to organize the workflow into separate nodes and conditional routes.

The system can route general AQI questions to the RAG pipeline and calculation-related questions to the AQI calculator.

Human approval is useful before executing the calculator workflow because it gives the user control over an action that affects the numerical result.

LangGraph also supports conversation state and checkpointing.

### Q10. What would you improve in the next version?

I would focus on:

1. Improving PDF table extraction and validation.
2. Preserving city, station and pollutant relationships during extraction.
3. Expanding historical AQI data coverage.
4. Improving retrieval evaluation using answer-quality and citation-quality metrics.
5. Adding more robust source verification.
6. Improving performance benchmarking.
7. Expanding monitoring and deployment reliability.

I would also investigate better city-level aggregation methods instead of relying only on simple station averages.

## 3. My Hardest-Problem Interview Story

**Situation:** CPCB AQI bulletins contained approximately 14 pages of structured tables. Extracting usable data from these PDFs was difficult because city names wrapped across lines and pollutant names were inconsistently formatted.

**Task:** I needed to convert the bulletin information into structured records while preserving the relationship between cities, stations and pollutant measurements.

**Action:** I treated the task as a data extraction and validation problem. I focused on normalizing pollutant labels, handling wrapped city names and validating the extracted values. I also kept AQI calculation separate from LLM generation by using CPCB breakpoint interpolation in Python.

**Result:** The project architecture separates document retrieval and natural-language explanation from deterministic AQI calculations. This reduces the risk of an LLM inventing numerical AQI results.

**Key lesson:** In an AI application, not every task should be delegated to an LLM. Structured extraction, validation and numerical calculations need deterministic logic.

## 4. Important Technical Terms to Revise

- **RAG:** Retrieves relevant information and provides it as context to an LLM.
- **Embedding:** A numerical vector representation of text.
- **ChromaDB:** A vector database used to store and retrieve embeddings.
- **Chunking:** Splitting documents into smaller pieces for retrieval.
- **Top-k:** Number of top-ranked retrieved chunks.
- **Precision@K:** Fraction of retrieved top-k results that are relevant.
- **Recall@K:** Fraction of relevant results retrieved in the top-k.
- **MRR:** Measures how highly the first relevant result is ranked.
- **Breakpoint interpolation:** Calculates a pollutant sub-index between defined concentration and AQI breakpoints.
- **LangGraph:** Framework for building stateful, graph-based agent workflows.
- **Human-in-the-loop:** Human approval or intervention within an automated workflow.
- **TTL cache:** Cache entries expire after a configured time.
- **Prompt injection:** Malicious or manipulative input attempting to override intended instructions.

## 5. Interview Honesty Checklist

Before the interview:

- Be able to explain every technology listed in the project.
- Distinguish implemented features from future improvements.
- Do not claim retrieval metrics prove answer accuracy.
- Do not claim the system eliminates hallucinations.
- Do not claim simple station averaging is an exact city-wide AQI representation.
- Explain the actual extraction challenges you encountered.
- Be prepared to demonstrate the API, Streamlit interface and calculator.
