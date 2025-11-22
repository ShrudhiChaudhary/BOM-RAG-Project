# Bank of Maharashtra Loan Information RAG System

A Retrieval-Augmented Generation (RAG) system designed to extract, process, and query loan-related information from Bank of Maharashtra (BOM) webpages using a combination of web scraping, embeddings, and a large language model (LLM).

---

## Table of Contents
1. [Project Overview](#project-overview)
2. [Setup Instructions](#setup-instructions)
3. [Folder Structure](#folder-structure)
4. [How to Run](#how-to-run)
5. [Architecture & Design Decisions](#architecture--design-decisions)
6. [Embedding Strategy Explained](#embedding-strategy-explained)
7. [Model Selection Justification](#model-selection-justification)
8. [Challenges & How You Solved Them](#challenges--how-you-solved-them)
9. [Improvements & Future Work](#improvements--future-work)
10. [Screenshots](#screenshots)
11. [Video Walkthrough Instructions](#video-walkthrough-instructions)

---

## Project Overview
This project provides an intelligent assistant to query and retrieve loan information from BOM’s web pages. Using a RAG pipeline, the system:
- Scrapes and cleans loan data from BOM websites.
- Generates vector embeddings of the textual data.
- Allows semantic queries via an LLM for precise, context-aware responses.

---

## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/ShrudhiChaudhary/BOM-RAG-Project.git
cd bom-loan-rag
``` 
### 2. Create and activate a virtual environment
```bash
python -m venv venv
```
#### Linux/Mac
```bash
source venv/bin/activate
```
#### Windows
```bash
venv\Scripts\activate
```
### 3. Install dependencies
```bash
pip install -r requirements.txt
```
#### Key libraries used:

##### requests, BeautifulSoup4, selenium, webdriver-manager — for web scraping

##### sentence-transformers — for embeddings (all-MiniLM-L6-v2)

##### ollama — to run phi3 LLM locally

##### tqdm — progress bars for scraping and processing

### 4. Prepare Urls

Create a urls.txt file containing one Bank of Maharashtra loan page URL per line.

### 5. Scapre Data
```bash
python scrape_bom.py --urls urls.txt --out_dir ../data/raw
# Optional: add --selenium for JS-heavy pages
```

## Folder Structure
```bash
bom-loan-rag/
│
├── data/
│ ├── raw/ # Raw scraped .txt files
│ ├── processed/ # Cleaned/processed documents
│ └── embeddings/ # Vector embeddings
│
├── scripts/
│ ├── scrape_bom.py # Web scraping script
│ └── preprocess.py # Optional text cleaning/preprocessing
│
├── models/
│ └── phi3/ # LLM-related files if needed
│
├── notebooks/ # Jupyter notebooks (optional)
├── requirements.txt
└── README.md
```
