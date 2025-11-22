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
