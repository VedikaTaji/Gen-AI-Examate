# AQIExplainer

## 1. Project Overview

AQIExplainer is a Python-based project designed to help users understand Air Quality Index (AQI) information across different cities in Maharashtra.

**The project provides:**
- City-wise AQI values.
- Air quality categories.
- Prominent pollutants.
- Monitoring station information.
- Searchable AQI records.
- City-wise air quality information.
- Cleaned and organized AQI data in JSON format.

## 2. Product

- An Air Quality Information and Explanation System.
- Helps users access and understand city-wise air quality information.
- Organizes AQI records for easy searching and analysis.
- Processes raw AQI data into structured records.

## 3. Target Users

- General public.
- Students.
- Researchers.
- People interested in air pollution and environmental awareness.

## 4. Problem Statement

Air pollution is a major environmental concern. Although AQI information is available, many people find it difficult to understand AQI values and their meanings.

**AQIExplainer aims to:**
- Organize air quality information.
- Make AQI data easier to understand.
- Help users search for city-wise air quality information.
- Improve awareness about environmental pollution.
- Process and organize raw air quality data for further analysis.

## 5. Data Source

**Central Pollution Control Board (CPCB), India**

- Organization: Central Pollution Control Board.
- Website: https://cpcb.nic.in/
- Data Type: Daily Air Quality Index (AQI) Bulletins.
- Coverage: Different cities across Maharashtra.
- Bulletin Date: 06 November 2026.
- Bulletin Time: 4 PM.
- Dataset: 20 Maharashtra city AQI records.

**Official Bulletin:**

https://cpcb.nic.in/National-Air-Quality-Index/

**Additional Raw Data:**
- Raw pollutant measurement data downloaded from the Maharashtra Pollution Control Board (MPCB) source.
- Includes pollutant measurements such as PM2.5, PM10, NO2, SO2 and CO.
- Original downloaded files are stored in `data/raw/`.

## 6. Technologies Used

- Python.
- CSV and JSON.
- Python Dataclasses.
- Requests Library.
- Exception Handling (try/except).
- Git.
- GitHub.
- Visual Studio Code (VS Code).
- Python Virtual Environment.

## 7. Planned Features

- Display AQI information for Maharashtra cities.
- Search AQI records using city names or keywords.
- Count cities according to AQI categories.
- Retrieve records using unique IDs.
- Provide an interactive command-line interface.
- Manage AQI records using reusable Python functions.
- Organize AQI data using lists and dictionaries.
- Clean and validate raw AQI data.
- Store processed AQI records in JSON format.
- Download AQI-related documents using Python requests.
- Handle invalid data rows and download errors.

## 8. Project Structure

```text
Gen-AI-Examate/
│
├── README.md
├── day01_intro.py
├── day01_menu.py
│
├── data/
│   ├── raw/
│   │   ├── AQI_Bulletin_20261106.pdf
│   │   ├── About_AQI.pdf
│   │   ├── aqi_data.csv
│   │   └── Raw_Data_2026_site_198_more_chowk_waluj_aurangabad_mpcb_1D.csv
│   │
│   ├── sample_records.py
│   └── records.json
│
├── app/
│   ├── __init__.py
│   ├── records.py
│   ├── cli.py
│   ├── models.py
│   ├── ingest.py
│   └── fetch.py
│
├── requirements.txt
└── .gitignore
```

## 9. Project Progress

- **Day 1:** Project introduction and menu-based application using Python variables, f-strings, input(), while loops and conditional statements.

- **Day 2:** Maharashtra AQI dataset creation with 20 city records, keyword searching, category counting, record retrieval and command-line interface development.

- **Day 3:** Downloaded CPCB AQI bulletin and raw pollutant data. Created `app/ingest.py` for CSV reading, data cleaning, validation and exception handling. Generated structured AQI records in `data/records.json`. Created `app/models.py` using Python dataclasses and developed `app/fetch.py` for downloading documents using the requests library.

- **GitHub:** Project version control and code management using Git and GitHub.

## 10. Author

- **Name:** Vedika
- **Project:** AQIExplainer

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
pip install -r requirements.txt
```

### Step 4: Run the AQI Data Analysis

```bash
python -m analysis.explore
```

### Step 5: Start the FastAPI Server

```bash
uvicorn app.main:app --reload
```

### Step 6: Open API Documentation

Open the following URL in your browser:

http://127.0.0.1:8000/docs

### Available API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Check API health |
| GET | `/records?limit=20` | Retrieve AQI records |
| GET | `/records/{id}` | Retrieve a record by ID |
| GET | `/search?q=Pune` | Search AQI records |
| POST | `/questions` | Ask AQI-related questions |

## 12. Day 4 – API Development and Smart Search

### S1: FastAPI Service
- Created a FastAPI application in `app/main.py`.
- Implemented the health-check endpoint.
- Added an endpoint to retrieve AQI records with a limit parameter.
- Implemented record retrieval by ID with HTTP 404 handling.
- Added an AQI search endpoint.
- Created a POST endpoint for AQI-related questions.

### S2: Data Analysis and Smart Search
- Created `analysis/explore.py` using pandas.
- Generated three facts from AQI records.
- Implemented TF-IDF vectorization in `app/smart_search.py`.
- Used cosine similarity to rank matching AQI records.
- Integrated smart search with the FastAPI search endpoint.

### Concepts Learned
- FastAPI
- REST API
- HTTP methods and status codes
- Pandas
- TF-IDF
- Cosine similarity
- API testing using Swagger UI