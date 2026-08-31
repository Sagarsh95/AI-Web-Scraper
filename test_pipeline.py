
import sys
import os
import shutil

# Ensure we can import from the parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), 'data'))
sys.path.append(os.path.dirname(__file__))

from data.cleaner import ContentCleaner
from data.storage import StorageManager

def test_pipeline():
    print("Starting Pipeline Test...")

    # 1. Test Cleaner
    raw_html = """
    <html>
        <head><title>Test Page</title><script>console.log('bad');</script></head>
        <body>
            <h1>Hello World</h1>
            <p>   This is a    messy   text.   </p>
        </body>
    </html>
    """
    print("Testing Cleaner...")
    cleaned = ContentCleaner.clean_html(raw_html)
    print(f"Cleaned Text: '{cleaned}'")
    
    expected = "Hello World This is a messy text."
    if cleaned == expected:
        print("✅ Cleaner Passed")
    else:
        print(f"❌ Cleaner Failed. Got: '{cleaned}'")

    # 2. Test Storage
    print("\nTesting Storage (ChromaDB)...")
    
    # Use a temporary directory for test DB
    test_db_dir = "./data/test_chroma_db"
    if os.path.exists(test_db_dir):
        shutil.rmtree(test_db_dir)
        
    storage = StorageManager(persist_directory=test_db_dir)
    
    metadata = {"url": "http://test.com", "source": "test_script"}
    doc_id = storage.save_document(cleaned, metadata)
    
    if doc_id:
        print(f"✅ Document saved with ID: {doc_id}")
    else:
        print("❌ Failed to save document")
        return

    # 3. Test Retrieval
    print("\nTesting Retrieval...")
    results = storage.query_documents("Hello World")
    
    if results and results['documents']:
        retrieved_doc = results['documents'][0][0]
        print(f"Retrieved: '{retrieved_doc}'")
        if "Hello World" in retrieved_doc:
            print("✅ Retrieval Passed")
        else:
            print("❌ Retrieval Content Mismatch")
    else:
        print("❌ Retrieval Failed (No results)")

    # Cleanup
    if os.path.exists(test_db_dir):
        try:
           shutil.rmtree(test_db_dir)
           print("\nCleanup Successful")
        except:
           pass

if __name__ == "__main__":
    test_pipeline()
