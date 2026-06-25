# 🎬 Semantic Movie Navigator

A high-performance semantic search engine for personalized movie recommendations 
using vector embeddings instead of keyword matching.

## 🚀 Overview
Bridges the gap between user intent and movie discovery. Search naturally — 
"mind-bending sci-fi with a twist ending" — and get semantically relevant results.

## 🛠️ System Architecture
- **Vectorization Engine:** Sentence Transformers (all-MiniLM-L6-v2) transforms 
  user queries into dense vector representations
- **Semantic Database:** ChromaDB for efficient vector similarity search
- **API Gateway:** Async FastAPI backend
- **Frontend:** Vanilla JS + Tailwind CSS

## 📊 How It Works
Unlike standard keyword search, this engine understands intent via cosine similarity 
between query and movie description embeddings. 1000+ movies indexed from TMDB API.

## 💻 Tech Stack
- **Language:** Python
- **ML/NLP:** Sentence-Transformers (all-MiniLM-L6-v2), ChromaDB
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
