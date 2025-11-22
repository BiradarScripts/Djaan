# 🔍 Multi-Document Embedding Search Engine

A lightweight, AI-powered search engine capable of semantic search over text documents. This project implements vector embeddings, efficient local caching, and a ranking algorithm to provide relevant search results with explanations.

Built for the **AI Engineer Intern Assignment**.

---

## 🚀 Features

* **Semantic Search:** Uses `sentence-transformers` (all-MiniLM-L6-v2) to understand query meaning, not just keywords.
* **Smart Caching:** Prevents redundant computations using SHA256 hashing and SQLite. If a document hasn't changed, its embedding is reused.
* **High-Performance Indexing:** Utilizes **FAISS (Facebook AI Similarity Search)** for efficient vector retrieval.
* **REST API:** A clean FastAPI backend to handle search requests.
* **Interactive UI:** A Streamlit dashboard for testing queries and visualizing results.
* **Ranking & Explanation:** Detailed scoring breakdown including cosine similarity and keyword overlap.
* **Bonus:** Query expansion using WordNet to find synonyms (e.g., "cosmos" → "universe").

---

## 📂 Project Structure

The project is modularized for scalability and maintainability.

```text
search_engine_project/
├── data/                  # Raw text documents (ignored by git)
├── storage/               # Persistent storage (SQLite DB & FAISS index)
├── src/
│   ├── __init__.py
│   ├── config.py          # Global configuration (paths, model names)
│   ├── text_processor.py  # Cleaning, hashing, and query expansion logic
│   ├── cache_manager.py   # SQLite interface for metadata caching
│   ├── embedder.py        # Logic to generate or retrieve embeddings
│   └── search_engine.py   # Core logic connecting FAISS, Embedder, and Ranking
├── main.py                # FastAPI application entry point
├── streamlit_app.py       # Frontend UI
├── setup_data.py          # Script to download sample dataset (20 Newsgroups)
├── requirements.txt       # Project dependencies
└── README.md              # Documentation
````

-----

## 🧹 Text Processing Pipeline (Design Choice)

Per the assignment requirements, all documents undergo a strict preprocessing pipeline before embedding:

1.  **HTML Removal:** Regex is used to strip any HTML tags (`<br>`, `<div>`, etc.) to ensure only content is embedded.

2.  **Normalization:** All text is converted to **lowercase** to maintain consistency.

3.  **Whitespace Cleaning:** Extra spaces, tabs, and newlines are collapsed into single spaces.

4.  **Hashing:** A **SHA256 hash** is generated from the cleaned text. This hash is used as a unique key in the SQLite cache to detect if a file has changed.

-----

## 🛠️ Installation & Setup

### 1\. Clone the Repository

```bash
git clone <repository-url>
cd search_engine_project
```

### 2\. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3\. Prepare the Data

Run the setup script to download the 20 Newsgroups dataset:

```bash
python setup_data.py
```

-----

## 🏃‍♂️ How to Run

### 1\. Start the Backend API

This initializes the embedding generation. The first run computes embeddings; subsequent runs use the cache.

```bash
uvicorn main:app --reload
```

*API available at: http://127.0.0.1:8000*

### 2\. Start the Frontend UI

Open a new terminal and run:

```bash
streamlit run streamlit_app.py
```

*UI available at: http://localhost:8501*

-----

## 🧠 Technical Architecture

### Caching Mechanism

The system uses SQLite (`storage/metadata.db`) as a key–value store:

  - **Key:** Document filename
  - **Value:** SHA256 hash, embedding blob, last-updated timestamp

**Logic:** If `Hash(New File) == Hash(Cached File)` → *Skip embedding to save computation.*

### Vector Search (FAISS)

  - **Library:** `faiss-cpu`
  - **Index Type:** `IndexFlatIP` (Inner Product)
  - **Why:** When vectors are L2-normalized, inner product = cosine similarity — ideal for semantic search.

-----

## 🛠️ API Reference

### **POST /search**

**Request Body:**

```json
{
  "query": "text to search",
  "top_k": 5
}
```

**Response:**

```json
{
  "results": [
    {
      "doc_id": "doc_014.txt",
      "score": 0.88,
      "preview": "The NASA orbit program...",
      "explanation": {
        "relevance_summary": "High cosine similarity (0.88)...",
        "overlap_ratio": 0.25
      }
    }
  ]
}
```

```

