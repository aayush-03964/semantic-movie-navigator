# 🎬 Semantic Movie Navigator

A high-performance semantic search engine for personalized movie recommendations that understands meaning, not just keywords.

## 🚀 Overview
Bridges the gap between user intent and movie discovery using vector embeddings. Search naturally — "mind-bending sci-fi with a twist ending" — and get semantically relevant results.

## 🛠️ System Architecture
- **Vectorization Engine:** Sentence Transformers (all-MiniLM-L6-v2) transforms user queries into dense vectors
- **Vector Database:** ChromaDB for efficient similarity search across 1000+ movies
- **API Gateway:** Async FastAPI backend
- **Frontend:** Vanilla JS + Tailwind CSS

## 💻 Tech Stack
- **Language:** Python
- **ML/NLP:** Sentence Transformers, ChromaDB
- **Backend:** FastAPI
- **Frontend:** Vanilla JS, Tailwind CSS
- **Data:** TMDB API

## ⚙️ Setup
```bash
pip install -r requirements.txt
```
Create a `.env` file:
TMDB_API_KEY=your_key_here

Run:
```bash
uvicorn main:app --reload
```

## 📊 How It Works
Movie descriptions are embedded into vectors at index time. User queries are embedded the same way and compared via cosine similarity in ChromaDB to return the most relevant results.
