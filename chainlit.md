# Autonomous Local RAG Engine 🧠

Welcome to the Retrieval-Augmented Generation interface. This frontend communicates directly with the n8n orchestration backend.

### ⚙️ Operating Instructions:
* **To Ingest:** Click the attachment icon below to upload a PDF. The engine will automatically extract, chunk, and vectorize the document using local embeddings.
* **To Query:** Type a question in the chat box. The engine will perform a similarity search in PostgreSQL and ground the LLM's response in your data.

---
*Powered by n8n, pgvector, Ollama, and Groq.*