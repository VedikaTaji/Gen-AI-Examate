# AQIExplainer

## 1. Project Overview

AQIExplainer is a Python-based project designed to help users understand Air Quality Index (AQI) information across different cities in Maharashtra.

The project combines data processing, search techniques, Large Language Models (LLMs), document retrieval and semantic search to make air quality information easier to access and understand.

**The project provides:**
- City-wise AQI values.
- Air quality categories.
- Prominent pollutants.
- Monitoring station information.
- Searchable AQI records.
- AI-powered AQI question answering.
- Document-based information retrieval.
- Cleaned and organized AQI data in JSON format.

## 2. Product

- An AI-powered Air Quality Information and Explanation System.
- Helps users access and understand city-wise air quality information.
- Organizes AQI records for easy searching and analysis.
- Processes raw AQI data into structured records.
- Uses LLMs to generate natural-language AQI explanations.
- Uses document retrieval and semantic search to find relevant AQI information.

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
- Split documents into smaller text chunks while preserving metadata.
- Store document embeddings in a persistent vector database.
- Retrieve relevant document chunks through semantic search.
- Evaluate search results using predefined AQI questions.

## 8. Project Structure

```text
Gen-AI-Examate/
│
├── README.md
├── requirements.txt
├── .gitignore
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
│   └── run_search_eval.py
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
    └── vectorstore.py
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
- Successfully generated 61 chunks from the available AQI documents.

**S2: Embeddings and Vector Database**
- Created `app/embed.py` for embedding generation and semantic retrieval.
- Implemented `app/vectorstore.py` using ChromaDB.
- Designed a persistent vector collection for AQI document chunks.
- Prepared semantic retrieval using document embeddings.
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
- Embedding model download encountered a network timeout.
- ChromaDB indexing, semantic API testing and retrieval evaluation are pending successful embedding generation and indexing.

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

### Step 6: Start the FastAPI Server

```bash
uvicorn app.main:app --reload
```

### Step 7: Open API Documentation

Open:

http://127.0.0.1:8000/docs

### Step 8: Build the Semantic Search Index

After the embedding model is available:

```bash
python -m app.vectorstore
```

### Step 9: Run Semantic Search Evaluation

After successfully building the vector index:

```bash
python -m eval.run_search_eval
```

## 12. Available API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Check API health |
| GET | `/records?limit=20` | Retrieve AQI records |
| GET | `/records/{id}` | Retrieve a record by ID |
| GET | `/search?q=Pune` | Search AQI records using smart search |
| POST | `/questions` | Ask AQI-related questions |
| POST | `/chat` | Generate AI-powered AQI responses |
| GET | `/search/semantic?q=air quality` | Search relevant AQI document chunks semantically |

*Note: The semantic search endpoint requires a successfully built ChromaDB index.*

## 13. Current AI Implementation

AQIExplainer combines multiple AI and information-retrieval techniques:

1. **Traditional Search:** TF-IDF vectorization and cosine similarity are used to rank matching AQI records.
2. **LLM Integration:** Groq and Google Gemini APIs are integrated for natural-language AQI question answering.
3. **Document Processing:** PDF, CSV and JSON documents are extracted and divided into overlapping chunks.
4. **Embedding-Based Retrieval:** ChromaDB is used as the planned persistent vector database for semantic retrieval.
5. **Retrieval Evaluation:** A set of 10 AQI questions is used to assess the relevance of retrieved document chunks.

The project is being developed incrementally, with each stage building on the previous implementation.

## 14. Future Enhancements

- Complete and validate the persistent ChromaDB vector index.
- Improve semantic retrieval accuracy.
- Implement Retrieval-Augmented Generation (RAG) by combining retrieved document chunks with LLM responses.
- Add source-based answers and document references.
- Improve document extraction and text cleaning.
- Add more historical AQI datasets.
- Develop an interactive frontend.
- Expand AQI coverage to more cities and locations.

## 15. Author

- **Name:** Vedika
- **Project:** AQIExplainer