
import sys
import os
import asyncio

# Ensure parent directory is in path
sys.path.append(os.path.join(os.path.dirname(__file__), 'ai_engine'))
sys.path.append(os.path.dirname(__file__))

from ai_engine.rag import RAGPipeline
from data.storage import StorageManager

async def test_rag():
    print("Starting RAG Test...")
    
    # 1. Seed some data
    print("Seeding test data...")
    storage = StorageManager()
    
    # Dummy sustainability content
    content = """
    EcoWear T-Shirt is made from 100% organic cotton certified by GOTS.
    It uses 50% less water than conventional cotton.
    Manufactured in a fair-trade facility in Portugal.
    """
    storage.save_document(content, metadata={"url": "http://ecowear.com/shirt", "source": "seed_data"})
    
    # 2. Run Analysis
    print("Running Analysis...")
    rag = RAGPipeline()
    query = "Is the EcoWear T-Shirt sustainable? What certifications does it have?"
    
    result = rag.run_analysis(query)
    
    print("\n--- AI Response ---")
    print(result['answer'])
    print("\n--- Sources ---")
    print(result['sources'])
    
    if "EcoWear" in result['answer'] and "GOTS" in result['answer']:
        print("\n✅ RAG Verification Passed")
    else:
        print("\n❌ RAG Verification Failed (Content mismatch)")

if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    asyncio.run(test_rag())
