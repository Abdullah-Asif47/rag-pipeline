# Autonomous Local RAG Engine

![Architecture: n8n + pgvector + Ollama + Chainlit](https://img.shields.io/badge/Architecture-n8n_%7C_pgvector_%7C_Ollama_%7C_Chainlit-blue)

A professional-grade Retrieval-Augmented Generation (RAG) pipeline designed to ingest, chunk, vectorize, and query unstructured documents. This architecture prioritizes local processing for data privacy and cost-efficiency, utilizing local GPU embeddings before routing context to a cloud LLM for final reasoning.

### 🎥 [Click Here to Watch the 60-Second Demo Video](https://youtu.be/38mgQdLn4H0)

## 🧠 System Architecture

The system is decoupled into two separate, asynchronous n8n workflows communicating with a centralized vector database and a Python frontend.

1. **The Ingestion Pipeline:** * Chainlit UI accepts a PDF upload and POSTs binary data to an n8n webhook.
   * n8n extracts raw text, sanitizes control characters, and chunks data.
   * Local Ollama (`nomic-embed-text`) generates 768-dimensional vector embeddings.
   * Vectors are stored securely in PostgreSQL using the `pgvector` extension.
2. **The Query Pipeline:**
   * User submits a query via Chainlit.
   * n8n vectorizes the query via Ollama.
   * PostgreSQL executes a similarity search (Cosine Distance) to retrieve the top 10 relevant chunks.
   * Chunks are aggregated and passed to Groq (Llama-3) with strict system prompts to prevent hallucination.
   * Grounded response is streamed back to the user UI.

## 🛠 Tech Stack
* **Orchestration:** n8n (Docker)
* **Database & Memory:** PostgreSQL 16 + pgvector (Docker)
* **Embeddings:** Ollama (`nomic-embed-text`) running locally on RTX 3070
* **LLM Inference:** Groq API / OpenRouter
* **Frontend:** Chainlit + Python

## 🚀 Quick Start Setup

### Prerequisites
* Docker & Docker Compose
* Python 3.10+
* Ollama installed locally

### 1. Spin up the Infrastructure
Boot the n8n orchestrator and the vector database.
bash
docker compose up -d


### 2. Start the Local Embedding Engine
Ensure Ollama is bound to all interfaces so the Docker containers can reach it.
bash
OLLAMA_HOST=0.0.0.0:11434 ollama serve &
ollama pull nomic-embed-text


### 3. Configure the Python Environment
Set up the isolated environment for the frontend UI.
bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt


### 4. Activate n8n Workflows
1. Navigate to `http://localhost:5678`.
2. Import the workflows (Ingestion and Query).
3. Set your Groq/OpenRouter API credentials in the HTTP Request nodes.
4. **Crucial:** Toggle both workflows to **Active** so the production webhooks listen continuously.

### 5. Launch the UI
Start the Chainlit frontend to interact with the engine.
bash
chainlit run app.py

*Navigate to `http://localhost:8000` to upload documents and query the RAG engine.*

## 🔒 Security Notes
* Database credentials are intentionally omitted from version control and managed via a local `.env` file. 
* Do not commit your `.env` or `venv/` directories.