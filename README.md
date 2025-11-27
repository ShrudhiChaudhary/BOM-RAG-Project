# Bank of Maharashtra Loan Information RAG System

A Retrieval-Augmented Generation (RAG) system designed to extract, process, and query loan-related information from Bank of Maharashtra (BOM) webpages using a combination of web scraping, embeddings, and a large language model (LLM).

---

## Table of Contents
1. [Project Overview](#project-overview)
2. [Setup Instructions](#setup-instructions)
3. [Folder Structure](#folder-structure)
4. [How to Run](#how-to-run)
5. [Architecture & Design Decisions](#architecture--design-decisions)

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
├── data_raw/ # Raw scraped .txt files from BOM website
├── data_processed/ # Cleaned and preprocessed text
│
├── rag/ # RAG pipeline related scripts
│ ├── build_vector_store.py # Code to create embeddings / vector store
│ └── local_rag.py # Code to query local RAG pipeline
│
├── scraper/ # Web scraping scripts and URLs
│ ├── scraper_bom.py # Scraper script
│ └── urls.txt # List of BOM loan page URLs
│
├── vector_store/ # Folder to store serialized vector embeddings
│
├── knowledge_base/ # Preprocessed knowledge base
│ ├── chunker.py # Script to chunk documents
│ ├── chunks.json # JSON file containing text chunks
│ └── loan_data.txt # Consolidated loan data text file
│
├── generate_files.py # Script to generate files for processing
├── main.py # Main script to run the RAG system
├── requirements.txt # Python dependencies
└── README.md # This README file
```
## How to Run

Follow these steps to run the BOM Loan Information RAG system:

---

### 1. Activate the virtual environment
### 2. Scrape raw data
```bash
python scraper/scrape_bom.py --urls scraper/urls.txt --out_dir data/raw --selenium
```
This will save raw .txt files into data_raw/.

### 3. Process documents and generate embeddings
```bash
python data/clean/clean_data.py --raw_dir data/raw --out_file knowledge_base/loan_data.txt
python generate_files.py
```
### 4. Chunk the data
```bash
python knowledge_base/chunker.py --input knowledge_base/loan_data.txt --out_json knowledge_base/chunks.json
```
### 5. Build vector store (FAISS)
```bash
python rag/build_vector_store.py --chunks knowledge_base/chunks.json --out_dir vector_store
```

### 6. Installing Free LLM
#### 1. Install Ollama
👉 https://ollama.com/download 

#### 2. Download a GOOD free model
```bash
ollama pull phi3  # fastest
```
### 7. Run main.py
```bash
python main.py
```

## Architecture & Design Decisions

### Architectural Decisions
The system was designed as a **RAG (Retrieval-Augmented Generation) pipeline** to allow semantic search over loan information. The architecture separates concerns into scraping, preprocessing, embedding, vector retrieval, and LLM query stages, making it modular, maintainable, and scalable.

### Libraries
- **Scraping:** `requests`, `BeautifulSoup4`, `selenium`, `webdriver-manager`  
  *Reason:* `requests` for static pages; Selenium for JS-heavy pages ensures complete coverage of dynamic content.  
- **Data Processing:** Standard Python libraries (`os`, `json`) and `tqdm` for progress visualization.  
- **RAG Pipeline:** `sentence-transformers` for embedding generation, `numpy` for vector operations, and custom scripts for retrieval and query handling.

### Data Strategy
- **Chunking:** Text documents are split into overlapping chunks (~500 tokens each).  
  *Reason:* Preserves context in each chunk while keeping them small enough for efficient embedding and retrieval.  
- **Storage:** Chunks are stored in `knowledge_base/chunks.json` and vector embeddings are saved in `vector_store/` for fast similarity search.

### Model Selection
- **Embedding Model:** `all-MiniLM-L6-v2` from Sentence Transformers  
  *Reason:* Provides a good trade-off between accuracy, speed, and resource efficiency for semantic search.  
- **LLM:** `phi3` running locally via Ollama  
  *Reason:* Local deployment ensures privacy, low latency, and full control over the model without API limits.

### AI Tools Used
- **phi3 (LLM):** For generating context-aware responses from retrieved chunks.  
- **Sentence Transformers (MiniLM):** For vector embeddings to enable semantic retrieval.  
- **Selenium:** Handles dynamic web pages during scraping.  

### Challenges Faced
- **Dynamic Pages:** Some BOM pages were JS-heavy, handled using Selenium fallback.  
- **Messy Data Formats:** HTML contained scripts, headers, footers, and ads, requiring custom cleaning logic.  
- **Large Documents:** Needed chunking to avoid memory issues and maintain context for embeddings.  

### Potential Improvements
- Automate incremental scraping for new loan pages.  
- Switch to a vector database like FAISS or Pinecone for scalable retrieval.  
- Enable multi-turn conversation for better user interaction.  
- Expand the system to support multiple banks for a unified loan information assistant.  

