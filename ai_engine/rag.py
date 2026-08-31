import logging
import sys
import os
import json
import re

# Add parent dir to path to find sibling modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from data.storage import StorageManager
from .llm import LLMClient
from .prompts import QA_PROMPT, CHAT_WITH_DATA_PROMPT

logger = logging.getLogger(__name__)

class RAGPipeline:
    def __init__(self):
        self.storage = StorageManager()
        self.llm_client = LLMClient(model_name="llama3.2")

    def run_analysis(self, query: str) -> dict:
        """
        Full RAG flow: Retrieve -> Augment -> Generate
        """
        # 1. Retrieve
        retrieved = self.storage.query_documents(query, n_results=3)
        context_str = ""
        sources = []
        
        if retrieved and retrieved['documents']:
            # Flatten list of lists
            docs = retrieved['documents'][0]
            context_str = "\n\n".join(docs)
            
            # Extract metadata (sources)
            if retrieved['metadatas']:
                metas = retrieved['metadatas'][0]
                sources = [m.get('url', 'unknown') for m in metas]

        if not context_str:
            return {
                "answer": "No relevant data found to answer this query.",
                "sources": []
            }

        # 2. Augment (Construct Prompt)
        final_prompt = QA_PROMPT.format(
            context=context_str,
            question=query
        )

        # 3. Generate
        logger.info(f"Sending prompt to LLM...")
        answer = self.llm_client.generate_response(final_prompt)
        
        return {
            "answer": answer,
            "sources": list(set(sources)) # Unique sources
        }

    def run_chat(self, query: str) -> dict:
        """
        RAG for Chat with JSON Chart extraction.
        """
        import time
        start_total = time.time()
        
        # 1. Retrieve
        start_retrieve = time.time()
        retrieved = self.storage.query_documents(query, n_results=3)
        context_str = ""
        sources = []
        
        MAX_CONTEXT_CHARS = 12000

        if retrieved and retrieved['documents']:
            docs_list = retrieved['documents'][0]
            
            accumulated_docs = []
            current_chars = 0
            
            for doc in docs_list:
                if len(doc) + current_chars > MAX_CONTEXT_CHARS:
                    # Take a slice to fit exactly or just stop
                    remaining = MAX_CONTEXT_CHARS - current_chars
                    if remaining > 100: # Only add if meaningful amount left
                        accumulated_docs.append(doc[:remaining] + "...[TRUNCATED]")
                    break
                
                accumulated_docs.append(doc)
                current_chars += len(doc)
                
            context_str = "\n---\n".join(accumulated_docs)
            
            if retrieved['metadatas']:
                metas = retrieved['metadatas'][0]
                # Slice sources to match the number of taken docs (approx)
                # It's safer to just include all probable sources or match index
                sources = [m.get('url', 'unknown') for m in metas]
        
        retrieve_duration = time.time() - start_retrieve
        logger.info(f"Retrieval took: {retrieve_duration:.2f}s")
        print(f"DEBUG: Retrieval took: {retrieve_duration:.2f}s")
        
        # 2. Augment with Chat Prompt
        final_prompt = CHAT_WITH_DATA_PROMPT.format(
            context=context_str,
            question=query
        )
        
        # 3. Generate
        start_gen = time.time()
        print(f"DEBUG: Starting LLM generation for prompt length: {len(final_prompt)} chars...")
        raw_response = self.llm_client.generate_response(final_prompt)
        gen_duration = time.time() - start_gen
        logger.info(f"Generation took: {gen_duration:.2f}s")
        print(f"DEBUG: Generation took: {gen_duration:.2f}s")
        
        # 4. Parse JSON Chart
        answer_text = raw_response
        chart_json = None
        
        # Regex to find JSON block
        json_match = re.search(r'\*\*\*CHART_JSON_START\*\*\*(.*?)\*\*\*CHART_JSON_END\*\*\*', raw_response, re.DOTALL)
        if json_match:
            json_str = json_match.group(1).strip()
            try:
                chart_json = json.loads(json_str)
                # Remove the JSON block from the text shown to user
                answer_text = raw_response.replace(json_match.group(0), "").strip()
            except json.JSONDecodeError:
                logger.error("Failed to parse Chart JSON from LLM response")
        
        return {
            "answer": answer_text,
            "sources": list(set(sources)),
            "chart": chart_json
        }

    def run_chat_stream(self, query: str):
        """
        Streaming RAG for Chat.
        Yields:
            1. JSON string with metadata (sources, etc.)
            2. Tokens (strings)
        """
        import time
        import json
        
        # 1. Retrieve
        start_retrieve = time.time()
        retrieved = self.storage.query_documents(query, n_results=3)
        context_str = ""
        sources = []
        
        MAX_CONTEXT_CHARS = 12000

        if retrieved and retrieved['documents']:
            docs_list = retrieved['documents'][0]
            accumulated_docs = []
            current_chars = 0
            
            for doc in docs_list:
                if len(doc) + current_chars > MAX_CONTEXT_CHARS:
                    remaining = MAX_CONTEXT_CHARS - current_chars
                    if remaining > 100:
                        accumulated_docs.append(doc[:remaining] + "...[TRUNCATED]")
                    break
                accumulated_docs.append(doc)
                current_chars += len(doc)
                
            context_str = "\n---\n".join(accumulated_docs)
            
            if retrieved['metadatas']:
                metas = retrieved['metadatas'][0]
                sources = [m.get('url', 'unknown') for m in metas]
        
        retrieve_duration = time.time() - start_retrieve
        logger.info(f"Retrieval took: {retrieve_duration:.2f}s")
        
        # 2. Yield Metadata Chunk First
        metadata = {
            "sources": list(set(sources)),
            "retrieval_time": retrieve_duration
        }
        # Yield metadata as a special JSON line followed by a separator or just strict JSON
        # For simplicity, we'll yield a JSON string with a specific prefix or just rely on the frontend to parse.
        # Let's try sending a JSON object as the first chunk, but we need to ensure the frontend distinguishes it.
        # Helper: We will yield a JSON string followed by a newline as the header.
        yield json.dumps({"type": "metadata", "data": metadata}) + "\n"

        # 3. Augment
        final_prompt = CHAT_WITH_DATA_PROMPT.format(
            context=context_str,
            question=query
        )
        
        # 4. Stream Generate
        logger.info(f"Starting stream generation...")
        for token in self.llm_client.stream_response(final_prompt):
            if token:
                yield token
