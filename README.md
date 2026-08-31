# AI Web Scraper

## Overview
AI Web Scraper is an AI-driven e-commerce intelligence platform for sustainable product analysis. It combines automated web scraping, content cleaning, semantic search, and a local RAG (Retrieval-Augmented Generation) pipeline to create grounded sustainability insights from product pages.

## Core Capabilities
- Scrape e-commerce product pages and search result links using Playwright.
- Clean and index scraped content into ChromaDB.
- Use a local Ollama LLM (`llama3.2`) to answer sustainability and product analysis queries.
- Provide a Streamlit dashboard for monitoring scraping, browsing analytics, and querying the knowledge base.
- Expose backend API endpoints for scraping, analysis, documents, and metrics.

## Repository Structure
- `backend/`: FastAPI backend and API routes.
- `frontend/streamlit/`: Streamlit-based UI and components.
- `ai_engine/`: RAG pipeline, prompts, and Ollama LLM wrapper.
- `scrapers/`: Scraper orchestrator and Playwright scraping logic.
- `data/`: Content cleaning and ChromaDB storage utilities.
- `requirements.txt`: Python dependencies.
- `README.md`: Project documentation.

## Prerequisites
- Python 3.9 or newer
- [Ollama](https://ollama.com/) installed locally
- Chromium browser via Playwright

## Setup
1. Create a Python virtual environment (recommended):
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Install Playwright browsers:
   ```bash
   playwright install chromium
   ```

4. Install and run Ollama, then pull the required model:
   ```bash
   ollama pull llama3.2
   ollama serve
   ```

## Running the Project

### Start the Backend
```bash
python backend/run.py
```
- Backend API listens on `http://127.0.0.1:8001`
- Health endpoint: `http://127.0.0.1:8001/health`

### Start the Frontend
```bash
streamlit run frontend/streamlit/app.py
```
- Streamlit UI is available at `http://localhost:8501`

### Optional: Use the API Directly
- `GET /health` — health check
- `POST /api/scrape` — scrape a URL
- `POST /api/analyze` — analyze a natural language query
- `POST /api/chat` — chat-style RAG interaction
- `GET /api/documents` — list stored documents
- `POST /api/metrics` — generate sustainability metrics

## Recommended Workflow
1. Start Ollama and ensure `llama3.2` is available.
2. Launch the backend:
   ```bash
   python backend/run.py
   ```
3. Launch the frontend:
   ```bash
   streamlit run frontend/streamlit/app.py
   ```
4. Use the UI to trigger scraping and request AI analysis.

## Notes
- The scraper supports multiple modes: `single_page`, `website`, and `search`.
- Scraped HTML is cleaned before saving into the vector store.
- The RAG pipeline retrieves top documents from ChromaDB and generates answers using local LLM inference.

## Troubleshooting
- If the frontend reports the backend as offline, verify `backend/run.py` is running and reachable at `http://127.0.0.1:8001`.
- If the LLM fails, confirm `ollama serve` is running and `llama3.2` is pulled.
- If scraping fails on Windows, ensure Playwright Chromium is installed and the process has network access.

## Screenshots
The UI supports exploratory scraping, raw HTML previews, extracted insights, and a dark-mode dashboard.

![Dashboard and Scraper Control](assets/screenshots/dashboard.png)

![Scraping Options and Keyword Extraction](assets/screenshots/keywords-and-ai.png)

![Content Summary and AI Insights](assets/screenshots/content-summary.png)

![Raw HTML Body Preview](assets/screenshots/raw-html.png)

> Place the screenshot images in `assets/screenshots/` with the file names shown above so the images render correctly.

## License
This project is provided as-is for development and research use.
