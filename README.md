# Minimal LangGraph RAG API

A small document-question-answering project built with FastAPI, LangGraph,
PageIndex, MongoDB, and Google Gemini.

## How it works

1. FastAPI accepts a question at `POST /query`.
2. LangGraph retrieves relevant passages from a PageIndex document tree stored
   in MongoDB.
3. Gemini answers using those passages.

See [ARCHITECTURE.md](ARCHITECTURE.md) for the request flow.

## Run with Docker

1. Copy `.env.example` to `.env` and set `GOOGLE_API_KEY` and
   `PAGEINDEX_API_KEY`.
2. Start MongoDB and the API:

   ```bash
   docker compose up --build
   ```

3. In another terminal, index a support PDF:

   ```bash
   python -m prep.index_docs --pdf path/to/support-guide.pdf --doc-id apple-support
   ```

4. Ask a question:

   ```bash
   curl.exe -X POST http://localhost:8000/query -H "Content-Type: application/json" -d "{\"query\":\"How do I reset my device?\"}"
   ```

   The API is also documented at `http://localhost:8000/docs`.

The document ID used for indexing must match `DOCUMENT_ID` in `.env`. When
using the bundled MongoDB service, its data is stored in the `mongo_data` Docker
volume.

To use an external MongoDB server instead, set `MONGODB_URI` in `.env`. Docker
Compose passes that value to the API; without it, the bundled MongoDB service is
used.

## Project structure

```text
main.py                         FastAPI app and /query endpoint
config.py                       Environment-based settings
graph/
  graph.py                      LangGraph retrieval-to-answer workflow
  state.py                      Data passed between graph nodes
  nodes/
    context_retrieval.py        MongoDB and PageIndex tree retrieval
    execution.py                Gemini answer generation
prep/
  index_docs.py                 Index a PDF and save its tree to MongoDB
prompts/
  generation.txt                Answer-generation prompt
tests/                          Unit tests
```

This is a minimal learning/demo project: authentication, rate limiting,
cross-request conversation memory, response caching, evaluation pipelines, and
deployment infrastructure have intentionally been left out.
