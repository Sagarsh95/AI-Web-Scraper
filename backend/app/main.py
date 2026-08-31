import sys
import asyncio

if sys.platform == "win32":
    # Required for Playwright on Windows
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="AI-Driven Web Intelligence API", version="1.0.0")

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "AI-Driven Web Intelligence System is running"}

@app.get("/health")
async def health_check():
    return {"status": "online", "component": "backend"}

from pydantic import BaseModel
class DebugPayload(BaseModel):
    text: str
    source: str

@app.post("/debug/store")
def debug_store(payload: DebugPayload):
    try:
        # Lazy import to avoid circular dependencies during initial setup
        import sys
        import os
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
        from data.storage import StorageManager
        
        storage = StorageManager()
        doc_id = storage.save_document(
            content=payload.text,
            metadata={"source": payload.source, "type": "debug"}
        )
        return {"status": "success", "doc_id": doc_id}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/api/documents")
def list_documents():
    try:
        # Lazy import
        import sys
        import os
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
        from data.storage import StorageManager
        
        storage = StorageManager()
        docs = storage.get_all_documents()
        return {"status": "success", "data": docs}
    except Exception as e:
        return {"status": "error", "message": str(e)}

class AnalyzePayload(BaseModel):
    query: str

@app.post("/api/analyze")
def analyze_query(payload: AnalyzePayload):
    try:
        # Lazy import
        import sys
        import os
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
        from ai_engine.rag import RAGPipeline
        
        rag = RAGPipeline()
        result = rag.run_analysis(payload.query)
        
        return {"status": "success", "data": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}

class ScrapePayload(BaseModel):
    url: str
    mode: str = "single_page"

@app.post("/api/scrape")
async def trigger_scrape(payload: ScrapePayload):
    try:
        # Lazy imports
        import sys
        import os
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
        
        from scrapers.orchestrator import ScraperOrchestrator
        from data.cleaner import ContentCleaner
        from data.storage import StorageManager
        
        # 1. Scrape
        orchestrator = ScraperOrchestrator()
        results = await orchestrator.start_scraping(payload.url, payload.mode)
        
        if isinstance(results, dict) and "error" in results:
             return {"status": "error", "message": results["error"]}
        
        # Ensure results is a list
        if not isinstance(results, list):
            results = [results]

        saved_ids = []
        preview_text = ""
        last_title = ""
        last_html = ""

        # 2. Process Each Page
        cleaner = ContentCleaner()
        storage = StorageManager()

        for page_data in results:
            if "error" in page_data:
                continue

            raw_html = page_data.get("content", "")
            last_html = raw_html # Capture for response
            current_url = page_data.get("url", payload.url)
            
            # Clean
            cleaned_text = cleaner.clean_html(raw_html)
            metadata_extracted = cleaner.extract_metadata(raw_html)
            
            # Merge metadata
            full_metadata = {
                "url": current_url,
                "title": metadata_extracted.get("title", ""),
                "mode": payload.mode,
                "source": "scraper_api"
            }
            
            # Store
            doc_id = storage.save_document(cleaned_text, full_metadata)
            if doc_id:
                saved_ids.append(doc_id)
                preview_text = cleaned_text[:200]
                last_title = full_metadata["title"]
        
        return {
            "status": "success", 
            "doc_ids": saved_ids, # Changed to plural
            "count": len(saved_ids),
            "title": last_title, # Title of last scraped page
            "preview": preview_text,
            "html_content": last_html
        }
        
    except Exception as e:
        return {"status": "error", "message": str(e)}

class MetricsPayload(BaseModel):
    query: str

@app.post("/api/metrics")
def generate_metrics(payload: MetricsPayload):
    try:
        # Lazy import 
        import sys
        import os
        import json
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
        from ai_engine.rag import RAGPipeline
        from ai_engine.prompts import METRICS_PROMPT
        
        # We reuse the RAG pipeline logic but invoke the specific metrics prompt
        
        rag = RAGPipeline()
        # 1. Retrieve
        retriever = rag.vector_store.as_retriever(search_kwargs={"k": 3})
        docs = retriever.invoke(payload.query)
        context = "\n\n".join([d.page_content for d in docs])
        
        if not context:
            return {"status": "success", "data": {"sustainability_score": 0, "pros": [], "cons": [], "summary": "No data found."}}
        
        # 2. Generate JSON
        prompt = METRICS_PROMPT.format(context=context)
        response_text = rag.llm_client.generate_response(prompt)
        
        # 3. Parse JSON
        # Clean potential markdown code blocks
        clean_json = response_text.replace("```json", "").replace("```", "").strip()
        try:
            metrics_data = json.loads(clean_json)
        except:
            # Fallback if LLM fails strict JSON
            metrics_data = {
                "sustainability_score": 50,
                "pros": ["Could not parse strictly"],
                "cons": [],
                "summary": response_text[:200]
            }
            
        return {"status": "success", "data": metrics_data}
        
    except Exception as e:
        return {"status": "error", "message": str(e)}

class ChatPayload(BaseModel):
    query: str

@app.post("/api/chat")
def chat_interaction(payload: ChatPayload):
    try:
        # Lazy import
        import sys
        import os
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
        from ai_engine.rag import RAGPipeline
        
        rag = RAGPipeline()
        result = rag.run_chat(payload.query)
        
        return {"status": "success", "data": result}
        
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/api/chat/stream")
def chat_interaction_stream(payload: ChatPayload):
    try:
        from fastapi.responses import StreamingResponse
        # Lazy import
        import sys
        import os
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
        from ai_engine.rag import RAGPipeline
        
        rag = RAGPipeline()
        
        return StreamingResponse(
            rag.run_chat_stream(payload.query),
            media_type="text/plain"
        )
        
    except Exception as e:
        return {"status": "error", "message": str(e)}
