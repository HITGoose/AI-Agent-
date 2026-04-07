# 🔬 SecuRAG: Academic Research Agent with Hybrid RAG Pipeline

> A production-style RAG Agent for academic literature research, featuring multi-stage retrieval, agentic routing, and automated evaluation.

![System Architecture](./SecuRAG_Retrieval_Pipeline-2026-02-06-094332.png)

## 📖 Introduction

**SecuRAG** is an intelligent research assistant built on a full agentic architecture. Unlike simple RAG systems, SecuRAG implements a **multi-stage retrieval pipeline** and an **autonomous intent router** that decides whether to retrieve from the knowledge base or respond directly.

### Key Features

* **Agentic Intent Router**: Autonomously classifies user queries into SEARCH or CHAT, achieving 85% accuracy on a 20-case test set.
* **Hybrid Retrieval Pipeline**: Combines BM25 keyword retrieval and dense vector search for higher recall.
* **CrossEncoder Reranking**: Two-stage retrieval with CrossEncoder re-scoring for improved precision.
* **Query Rewriting**: LLM-based coreference resolution to handle multi-turn ambiguous queries.
* **Multi-turn Memory**: Session-based conversation history management.
* **LLM-as-a-Judge Eval**: Automated evaluation of answer relevance and completeness.
* **Local Privacy Mode**: Fully offline using Ollama + ChromaDB. Zero data egress.
* **Microservices Architecture**: Decoupled FastAPI backend + Streamlit frontend, Docker-ready.

---

## 📊 Performance

| Metric | Result |
|--------|--------|
| Intent Router Accuracy | 85% (17/20 test cases) |
| Retrieval | BM25 + Vector hybrid, top-5 recall |
| Reranking | CrossEncoder ms-marco-MiniLM-L-6-v2 |
| Eval | LLM-as-a-Judge (relevance + completeness) |

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.10+
- Ollama installed and running
- Docker (optional)

### 1. Clone & Install

git clone https://github.com/HITGoose/SecuRAG-Agent.git
cd SecuRAG-Agent
pip install -r requirements.txt

### 2. Configure Environment

APP_MODE=local
OLLAMA_HOST=http://localhost:11434
DEEPSEEK_API_KEY=your_key

### 3. Pull Local Model

ollama pull deepseek-r1:1.5b

### 4. Run

Option A: Docker
docker-compose up

Option B: Manual
Terminal 1: python api_server.py
Terminal 2: streamlit run frontend.py

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| LLM | DeepSeek / Ollama |
| Vector DB | ChromaDB |
| Retrieval | BM25 + Dense Vector |
| Reranking | CrossEncoder |
| Backend | FastAPI |
| Frontend | Streamlit |
| Deployment | Docker |

---

## 📁 Project Structure

securag_engine.py    - Core RAG Agent engine
hybrid_retriever.py  - BM25 + Vector hybrid retrieval
reranker.py          - CrossEncoder reranking
security_guard.py    - Input sanitization
pdf_loader.py        - PDF ingestion pipeline
api_server.py        - FastAPI backend
frontend.py          - Streamlit UI
test_intent.py       - Intent router evaluation
test_eval.py         - LLM-as-a-Judge evaluation
Dockerfile
docker-compose.yml
