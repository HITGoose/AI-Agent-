# 🛡️ SecuRAG: Secure RAG Agent with Hybrid Defense

> **A Master's Project Prototype for Multimedia Security & Adversarial Defense**

![System Architecture](./system_architecture.png) 
*(Please replace with your actual diagram file name)*

## 📖 Introduction
**SecuRAG** is a Retrieval-Augmented Generation (RAG) system designed with a "Security-First" approach. Unlike traditional RAG systems, SecuRAG implements a **Hybrid Defense Layer** to filter adversarial prompts (e.g., Jailbreak attacks) before they reach the LLM or Knowledge Base.

### Key Features
* **Hybrid Security Layer**: Combines deterministic Regex filters with a semantic AI Firewall (DeepSeek/Llama3).
* **Local Privacy Mode**: Fully functional offline using Ollama and local ChromaDB. No data egress.
* **Dynamic Knowledge Base**: Supports PDF ingestion via a decoupled API.
* **User-Friendly UI**: A Streamlit-based dashboard with real-time audit visualization.

---

## Architecture
The system follows a **Microservices Architecture**:

1.  **Frontend**: Streamlit (Port 8501) - User Interface.
2.  **Backend**: FastAPI (Port 8000) - API Gateway & Business Logic.
3.  **Engine**: SecuRAG Engine - Orchestrates Ollama and ChromaDB.
4.  **Database**: ChromaDB (Persistent SQLite) - Vector storage.

---

## Installation & Setup

### Prerequisites
* Python 3.10+
* [Ollama](https://ollama.com/) installed and running.
* Model pulled: `ollama pull deepseek-r1:1.5b` (or your chosen model).

### 1. Clone & Install Dependencies
```bash
# Install required Python packages
pip install -r requirements.txt