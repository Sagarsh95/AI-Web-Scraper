import chromadb
from chromadb.config import Settings
import uuid
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class StorageManager:
    def __init__(self, persist_directory: str = "./data/chroma_db"):
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection = self.client.get_or_create_collection(name="scraped_data")

    def save_document(self, content: str, metadata: dict):
        """
        Saves a document to the vector store.
        Note: Without an embedding function provided, Chroma uses a default basic one.
        Phase 4 will introduce a better local embedding model.
        """
        try:
            doc_id = str(uuid.uuid4())
            # Ensure metadata values are strings or simple types
            cleaned_metadata = {k: str(v) for k, v in metadata.items()}
            cleaned_metadata["timestamp"] = datetime.now().isoformat()
            
            self.collection.add(
                documents=[content],
                metadatas=[cleaned_metadata],
                ids=[doc_id]
            )
            return doc_id
        except Exception as e:
            logger.error(f"Error saving document: {e}")
            return None

    def get_document(self, doc_id: str):
        """Retrieve a specific document by ID."""
        try:
            result = self.collection.get(ids=[doc_id])
            if result and result['documents']:
                return {
                    "id": doc_id,
                    "content": result['documents'][0],
                    "metadata": result['metadatas'][0]
                }
            return None
        except Exception:
            return None

    def get_all_documents(self):
        """Retrieve all documents metadata (lighter query)."""
        try:
            # We fetch everything but not embeddings to save bandwidth
            result = self.collection.get(include=["metadatas", "documents"])
            docs = []
            if result and result['ids']:
                for i, doc_id in enumerate(result['ids']):
                    docs.append({
                        "id": doc_id,
                        "metadata": result['metadatas'][i],
                        # Return snippet of content
                        "preview": result['documents'][i][:100] + "..." if result['documents'][i] else ""
                    })
            return docs
        except Exception as e:
            print(f"Error fetching docs: {e}")
            return []

    def query_documents(self, query_text: str, n_results: int = 2):
        """
        Retrieves relevant documents.
        """
        try:
            results = self.collection.query(
                query_texts=[query_text],
                n_results=n_results
            )
            return results
        except Exception as e:
            logger.error(f"Error querying documents: {e}")
            return None
