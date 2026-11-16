# AQIExplainer

## 1. Project Overview

AQIExplainer is a Python-based project designed to help users understand Air Quality Index (AQI) information across different cities in Maharashtra.

The project combines data processing, search techniques, Large Language Models (LLMs), document retrieval, semantic search and Retrieval-Augmented Generation (RAG) to make air quality information easier to access and understand.

**The project provides:**

- City-wise AQI values.
- Air quality categories.
- Prominent pollutants.
- Monitoring station information.
- Searchable AQI records.
- AI-powered AQI question answering.
- Document-based information retrieval.
- Semantic search using vector embeddings.
- RAG-based answers with document citations.
- Cleaned and organized AQI data in JSON format.

## 2. Product

- An AI-powered Air Quality Information and Explanation System.
- Helps users access and understand city-wise air quality information.
- Organizes AQI records for easy searching and analysis.
- Processes raw AQI data into structured records.
- Uses LLMs to generate natural-language AQI explanations.
- Uses document retrieval and semantic search to find relevant AQI information.
- Uses RAG to generate answers grounded in retrieved documents.

## 3. Target Users

- General public.
- Students.
- Researchers.
- People interested in air pollution and environmental awareness.

## 4. Problem Statement

Air pollution is a major environmental concern. Although AQI information is publicly available, many people find it difficult to understand AQI values, their categories and the pollutants responsible for air quality conditions.

**AQIExplainer aims to:**

- Organize air quality information.
- Make AQI data easier to understand.
- Help users search for city-wise air quality information.
- Generate understandable answers to AQI-related questions.
- Improve awareness about environmental pollution.
- Process and organize raw air quality data for further analysis.
- Provide document-grounded answers with source references.

## 5. Data Sources

### Central Pollution Control Board (CPCB), India

- Organization: Central Pollution Control Board.
- Website: https://cpcb.nic.in/
- Data Type: Daily Air Quality Index (AQI) Bulletins.
- Coverage: Different cities across Maharashtra.
- Bulletin Date: 06 November 2026.
- Bulletin Time: 4 PM.
- Dataset: 20 Maharashtra city AQI records.

**Official Bulletin:**

https://cpcb.nic.in/National-Air-Quality-Index/

### Additional Raw Data

- Raw pollutant measurement data downloaded from the Maharashtra Pollution Control Board (MPCB) source.
- Includes pollutant measurements such as PM2.5, PM10, NO2, SO2 and CO.
- Original downloaded files are stored in `data/raw/`.

## 6. Technologies Used

### Programming and Backend

- Python
- FastAPI
- Uvicorn
- Python Dataclasses
- Exception Handling

### Data Processing and Search

- CSV and JSON
- Pandas
- Scikit-learn
- TF-IDF Vectorization
- Cosine Similarity
- PyPDF

### Generative AI and Retrieval

- Large Language Models (LLMs)
- Groq API
- Google Gemini API
- Prompt Engineering
- Embeddings
- ChromaDB
- Semantic Search
- Document Chunking
- Retrieval-Augmented Generation (RAG)
- Source-based Citations

### Development Tools

- Git and GitHub
- Visual Studio Code
- Python Virtual Environment
- Python-dotenv
- Swagger UI

## 7. Main Features

- Display AQI information for Maharashtra cities.
- Search AQI records using city names or keywords.
- Count cities according to AQI categories.
- Retrieve records using unique IDs.
- Process and clean raw AQI data.
- Store processed AQI records in JSON format.
- Download AQI-related documents.
- Generate natural-language answers using LLMs.
- Support Groq and Gemini as LLM providers.
- Extract text from PDF, CSV and JSON documents.
- Split documents into smaller overlapping text chunks while preserving metadata.
- Generate embeddings for document chunks.
- Store document embeddings in a persistent ChromaDB vector database.
- Retrieve relevant document chunks through semantic search.
- Generate RAG-based answers using retrieved document context.
- Provide source references with generated answers.
- Return "I don't know" when the requested historical information is unavailable.
- Evaluate retrieval performance using predefined AQI questions and different configurations.

## 8. Project Structure

```text
Gen-AI-Examate/
│
├── README.md
├── requirements.txt
├── .gitignore
├── .env.example
│
├── day01_intro.py
├── day01_menu.py
│
├── docs/
│   ├── how_llms_work.md
│   └── user_questions.md
│
├── analysis/
│   └── explore.py
│
├── eval/
│   ├── eval_set.json
│   ├── run_eval.py
│   ├── run_search_eval.py
│   ├── search_results.md
│   ├── results.json
│   ├── results.md
│   └── prompt_compare.md
│
├── data/
│   ├── raw/
│   │   ├── AQI_Bulletin_20261106.pdf
│   │   ├── About_AQI.pdf
│   │   ├── aqi_data.csv
│   │   └── Raw_Data_2026_site_198_more_chowk_waluj_aurangabad_mpcb_1D.csv
│   │
│   ├── sample_records.py
│   ├── records.json
│   └── chroma/                 # Local ChromaDB storage (not committed)
│
└── app/
    ├── __init__.py
    ├── records.py
    ├── cli.py
    ├── models.py
    ├── ingest.py
    ├── fetch.py
    ├── main.py
    ├── smart_search.py
    ├── llm.py
    ├── chunking.py
    ├── embed.py
    ├── vectorstore.py
    └── rag.py
```

## 9. Project Progress

### Day 1 – Python Fundamentals

- Created the project introduction.
- Developed a menu-based application.
- Practised Python variables, f-strings, input(), while loops and conditional statements.

### Day 2 – AQI Dataset and Search

- Created a Maharashtra AQI dataset containing 20 city records.
- Implemented keyword searching.
- Implemented AQI category counting.
- Added record retrieval functionality.
- Developed a command-line interface.

### Day 3 – Data Ingestion and Processing

- Downloaded the CPCB AQI bulletin and raw pollutant data.
- Created `app/ingest.py` for CSV reading, data cleaning and validation.
- Generated structured AQI records in `data/records.json`.
- Created `app/models.py` using Python dataclasses.
- Developed `app/fetch.py` for downloading documents using the Requests library.
- Practised exception handling and invalid-data management.

### Day 4 – API Development and Smart Search

**S1: FastAPI Service**

- Created a FastAPI application in `app/main.py`.
- Implemented health-check functionality.
- Added an endpoint to retrieve AQI records with a limit parameter.
- Implemented record retrieval by ID with HTTP 404 handling.
- Added an AQI search endpoint.
- Created a POST endpoint for AQI-related questions.

**S2: Data Analysis and Smart Search**

- Created `analysis/explore.py` using Pandas.
- Generated three facts from AQI records.
- Implemented TF-IDF vectorization in `app/smart_search.py`.
- Used cosine similarity to rank matching AQI records.
- Integrated smart search with the FastAPI application.

**Concepts Learned:**

- FastAPI and REST APIs.
- HTTP methods and status codes.
- Pandas.
- TF-IDF.
- Cosine similarity.
- API testing using Swagger UI.

### Day 5 – LLM Fundamentals and Documentation

**S1: Understanding Large Language Models**

- Studied Large Language Model fundamentals.
- Learned how tokenization converts text into smaller tokens.
- Understood embeddings and numerical representations of text.
- Studied Transformer architecture.
- Learned about the self-attention mechanism.
- Understood next-token prediction and response generation.
- Created `docs/how_llms_work.md` with a workflow diagram.

**S2: AQIExplainer User Questions**

- Created `docs/user_questions.md`.
- Added 10 realistic questions based on AQIExplainer functionality.
- Identified questions that can and cannot be answered using the current dataset.
- Included a historical AQI question requiring 30 days of data, which is not currently available.

**Checkpoint 1**

- Successfully ran the FastAPI application.
- Verified API endpoints using Swagger UI.
- Tested AQI record retrieval, search and question-answering functionality.
- Created the Git checkpoint `checkpoint-1`.

**Concepts Learned:**

- LLMs.
- Tokenization and embeddings.
- Transformer architecture.
- Self-attention.
- Next-token prediction.
- Dataset limitations.
- Git checkpoint tagging.

### Day 6 – LLM Integration

**S1: LLM Provider Integration**

- Implemented `app/llm.py` for LLM-based AQI question answering.
- Integrated the Groq API.
- Integrated the Google Gemini API.
- Added environment-variable configuration using Python-dotenv.
- Implemented provider selection through configuration.
- Created prompt-based response generation.
- Added JSON response parsing and error handling.

**S2: AQI Question Answering**

- Connected LLM response generation with AQI records.
- Used project data as context for answering user questions.
- Generated structured responses containing:
  - Answer
  - Confidence
  - Follow-up question
- Tested AQI question answering using Groq.
- Verified the `/chat` API endpoint through FastAPI.

**Concepts Learned:**

- LLM API integration.
- Groq and Gemini.
- Prompt engineering.
- Environment variables.
- JSON response parsing.
- Context-based question answering.
- API integration and testing.

### Day 7 – Document Chunking, Embeddings and Semantic Search

**S1: Document Processing and Chunking**

- Created `app/chunking.py`.
- Implemented text extraction from PDF, CSV and JSON documents.
- Split extracted text into smaller overlapping chunks.
- Preserved document metadata, including:
  - Source
  - Title
  - Page or row number
  - Chunk index
- Successfully generated 61 chunks using the default configuration of 900 characters and 150-character overlap.

**S2: Embeddings and Vector Database**

- Created `app/embed.py` for embedding generation and semantic retrieval.
- Implemented `app/vectorstore.py` using ChromaDB.
- Created a persistent vector collection named `aqi_documents`.
- Generated embeddings and successfully indexed all 61 document chunks.
- Added the `GET /search/semantic` API endpoint in `app/main.py`.
- Created `eval/run_search_eval.py` to evaluate retrieval against 10 AQI questions.
- Prepared `eval/search_results.md` for recording search results.

**Concepts Learned:**

- Document chunking.
- Chunk overlap.
- Document metadata.
- Text embeddings.
- Semantic search.
- Vector databases.
- ChromaDB.
- Retrieval evaluation.

**Day 7 Status:**

- Document extraction and chunking successfully completed.
- Generated 61 document chunks.
- ChromaDB embedding generation successfully completed.
- Indexed all 61 chunks in the persistent `aqi_documents` collection.
- Verified collection access and document count.
- Prepared the semantic search API and evaluation workflow.

### Day 8 – Retrieval-Augmented Generation (RAG) and Evaluation

**S1: RAG Implementation**

- Created `app/rag.py` for Retrieval-Augmented Generation.
- Implemented document retrieval using ChromaDB.
- Retrieved relevant document chunks based on user questions.
- Integrated retrieved context with Groq/Gemini LLM response generation.
- Added source-based citations containing document title, source and page/row information.
- Implemented confidence levels in RAG responses.
- Added `POST /ask` endpoint in `app/main.py`.
- Tested RAG through FastAPI Swagger UI.
- Verified that answerable AQI questions generate document-grounded responses with citations.
- Tested an unavailable historical AQI question and verified that the system returns `I don't know` with low confidence and no citations.

**S2: Retrieval Evaluation**

- Created `eval/eval_set.json` containing 15 AQI evaluation questions.
- Included an unanswerable historical AQI question (Q6).
- Created `eval/run_eval.py` to compare two retrieval configurations.
- Modified `app/chunking.py` to support configurable chunk sizes and overlap.
- Modified `app/vectorstore.py` to support multiple ChromaDB collections.
- Created separate evaluation collections:
  - `aqi_eval_a`
  - `aqi_eval_b`
- Evaluated both configurations using the 15-question dataset.
- Generated evaluation reports in `eval/results.json` and `eval/results.md`.

**Evaluation Configurations**

| Parameter | Configuration A | Configuration B |
|---|---:|---:|
| Chunk Size | 900 | 500 |
| Overlap | 150 | 100 |
| Top-k | 3 | 5 |
| Total Chunks | 61 | 79 |
| Keyword Hits | 14/14 | 14/14 |
| Retrieval Hit Rate | 100% | 100% |
| Mean Similarity | 0.5490 | 0.5191 |

**Winning Configuration: Configuration A**

- Both configurations achieved a 100% keyword-based retrieval hit rate.
- Configuration A achieved a higher mean similarity score of 0.5490 compared with 0.5191 for Configuration B.
- Configuration A was selected based on its higher mean similarity score while maintaining the same keyword hit rate.

**Q6 Abstention Test**

Question: How has the AQI of Pune changed over the last 30 days?

Expected response: `I don't know`

Observed response: `I don't know`

- Confidence: Low
- Citations: None

**Evaluation Method Note:**

Keyword hit rate checks whether at least one expected keyword appears in the retrieved chunks. It is a retrieval relevance proxy and does not establish factual answer accuracy. Mean similarity is used as a supporting comparison metric.

**Concepts Learned:**

- Retrieval-Augmented Generation.
- Context retrieval.
- LLM-based answer generation.
- Source-based citations.
- Retrieval and generation workflows.
- ChromaDB collection management.
- Configurable chunking.
- Top-k retrieval.
- Evaluation datasets.
- Retrieval hit rate and similarity scores.
- Abstention for unavailable information.

## 10. GitHub and Version Control

- Maintained the project using Git and GitHub.
- Used Git commits to track daily development.
- Organized project files into reusable modules.
- Used Git checkpoints to maintain development progress.
- Excluded environment files and local database storage from version control.

## 11. How to Run the Project

### Step 1: Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd Gen-AI-Examate
```

### Step 2: Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### Step 3: Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

Create a `.env` file in the project root and add your own API credentials:

```env
LLM_PROVIDER=groq

GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=openai/gpt-oss-20b

GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=your_gemini_model_here
```

Do not upload your actual `.env` file or API keys to GitHub.

### Step 5: Run AQI Data Analysis

```bash
python -m analysis.explore
```

### Step 6: Build the Document Chunks

```bash
python -m app.chunking
```

### Step 7: Build the ChromaDB Semantic Search Index

```bash
python -m app.vectorstore
```

This creates or rebuilds the default `aqi_documents` collection using 900-character chunks and 150-character overlap.

### Step 8: Start the FastAPI Server

```bash
uvicorn app.main:app --reload
```

### Step 9: Open API Documentation

Open:

http://127.0.0.1:8000/docs

Use Swagger UI to test the available API endpoints, including semantic search and RAG question answering.

### Step 10: Run Semantic Search Evaluation

```bash
python -m eval.run_search_eval
```

### Step 11: Run RAG Retrieval Evaluation

Stop the running FastAPI server if necessary, then execute:

```bash
python -m eval.run_eval
```

This builds two separate evaluation collections, compares the retrieval configurations and generates:

- `eval/results.json`
- `eval/results.md`

## 12. Available API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Check API health |
| GET | `/records?limit=20` | Retrieve AQI records |
| GET | `/records/{id}` | Retrieve a record by ID |
| GET | `/search?q=Pune` | Search AQI records using smart search |
| POST | `/questions` | Ask AQI-related questions |
| POST | `/chat` | Generate AI-powered AQI responses using LLMs |
| GET | `/search/semantic?q=air quality` | Search relevant AQI document chunks semantically |
| POST | `/ask` | Generate RAG-based answers with document citations |

**Note:** The semantic search and RAG endpoints require a successfully built ChromaDB index.

## 13. Current AI Implementation

AQIExplainer combines multiple AI and information-retrieval techniques:

1. **Traditional Search:** TF-IDF vectorization and cosine similarity are used to rank matching AQI records.
2. **LLM Integration:** Groq and Google Gemini APIs are integrated for natural-language AQI question answering.
3. **Document Processing:** PDF, CSV and JSON documents are extracted and divided into overlapping chunks.
4. **Embedding-Based Retrieval:** ChromaDB stores document embeddings and supports semantic retrieval.
5. **Retrieval-Augmented Generation:** Retrieved document chunks are passed as context to an LLM to generate grounded answers.
6. **Source-Based Citations:** RAG responses include references to retrieved document sources.
7. **Retrieval Evaluation:** A 15-question evaluation dataset compares different chunking and top-k configurations using keyword hit rate and mean similarity.

The current evaluation selected Configuration A (900-character chunks, 150-character overlap and top-k 3), based on its higher mean similarity score while maintaining a 100% keyword-based retrieval hit rate.

The project is being developed incrementally, with each stage building on the previous implementation.

## 14. Future Enhancements

- Improve semantic retrieval accuracy and relevance evaluation.
- Introduce stronger answer-quality evaluation beyond keyword matching.
- Improve document extraction and text cleaning.
- Add more historical AQI datasets.
- Improve citation selection and source verification.
- Add confidence-based retrieval and abstention improvements.
- Develop an interactive frontend.
- Expand AQI coverage to more cities and locations.
- Add more AQI-related datasets and document sources.

## 15. Author

- **Name:** Vedika
- **Project:** AQIExplainer
