
import requests
import time
import sys

BASE_URL = "http://localhost:8000"

def test_full_system(target_url="http://example.com"):
    print(f"🔬 Starting Integration Test against {BASE_URL}")

    # 1. Health Check
    try:
        resp = requests.get(f"{BASE_URL}/health")
        if resp.status_code == 200:
            print("✅ Backend Health: Online")
        else:
            print(f"❌ Backend Unhealthy: {resp.status_code}")
            return
    except Exception as e:
        print(f"❌ Failed to connect to Backend: {e}")
        return

    # 2. Scrape
    print(f"\n🕷️ Triggering Scrape for {target_url}...")
    try:
        start_time = time.time()
        scrape_payload = {"url": target_url, "mode": "single_page"}
        scrape_resp = requests.post(f"{BASE_URL}/api/scrape", json=scrape_payload, timeout=60)
        
        if scrape_resp.status_code == 200:
            data = scrape_resp.json()
            if data.get('status') == 'success':
                print(f"✅ Scraping Successful ({time.time() - start_time:.2f}s)")
                print(f"   DocID: {data.get('doc_id')}")
            else:
                print(f"❌ Scraping Logic Failed.")
                print(f"   Message: {data.get('message')}")
                # Print full error data if available
                if 'error' in data:
                    print(f"   Full Error: {data['error']}")
                return
        else:
            print(f"❌ Scraping API Error: {scrape_resp.status_code}")
            print(f"   Body: {scrape_resp.text}")
            return
    except Exception as e:
        print(f"❌ Scraping Exception: {e}")
        return

    # 3. Analyze (RAG)
    print("\n🧠 Testing AI Analysis...")
    queries = [
        "What is the title of the page?",
        "Summarize the content."
    ]
    
    for query in queries:
        try:
            print(f"   Query: '{query}'")
            rag_payload = {"query": query}
            rag_resp = requests.post(f"{BASE_URL}/api/analyze", json=rag_payload, timeout=60)
            
            if rag_resp.status_code == 200:
                data = rag_resp.json()
                if data['status'] == 'success':
                    answer = data['data']['answer']
                    print(f"   ✅ AI Answer: {answer[:100]}...") 
                else:
                    print(f"   ❌ AI Logic Failed: {data.get('message')}")
            else:
                print(f"   ❌ AI API Error: {rag_resp.status_code}")
        except Exception as e:
            print(f"   ❌ AI Exception: {e}")

if __name__ == "__main__":
    test_full_system("http://example.com")
