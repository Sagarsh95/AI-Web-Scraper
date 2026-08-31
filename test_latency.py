import requests
import time

BACKEND_URL = "http://localhost:8001"

def test_latency():
    print(f"Testing chat latency at {BACKEND_URL}/api/chat ...")
    # This is the query the user complained about
    payload = {"query": "list all products in table format"}
    
    try:
        start = time.time()
        print("Sending request (this may take a while)...")
        response = requests.post(f"{BACKEND_URL}/api/chat", json=payload, timeout=600)
        duration = time.time() - start
        
        print(f"Status: {response.status_code}")
        print(f"Total Duration: {duration:.2f}s")
        
        if response.status_code == 200:
            data = response.json().get("data", {})
            answer = data.get("answer", "")
            print(f"Response length: {len(answer)} chars")
        else:
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    test_latency()
