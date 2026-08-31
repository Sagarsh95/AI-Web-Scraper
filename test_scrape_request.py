import requests
import time
import sys

def test_scrape():
    url = "http://127.0.0.1:8001/api/scrape"
    payload = {
        "url": "laptops", 
        "mode": "search"
    }
    
    print("Sending scrape request...")
    try:
        response = requests.post(url, json=payload, timeout=60)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text[:500]}")
        
        if response.status_code == 200:
            print("SUCCESS: Scrape request verified.")
        else:
            print("FAILURE: Scrape request returned error.")
            
    except Exception as e:
        print(f"EXCEPTION: {e}")

if __name__ == "__main__":
    # Wait for server to potentially start
    time.sleep(2)
    test_scrape()
