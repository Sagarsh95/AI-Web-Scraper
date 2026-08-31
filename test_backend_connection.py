import requests
import time
import threading

BACKEND_URL = "http://localhost:8001"

def test_health():
    print(f"Testing health check at {BACKEND_URL}/health ...")
    try:
        start = time.time()
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        duration = time.time() - start
        print(f"Health check status: {response.status_code}")
        print(f"Duration: {duration:.2f}s")
    except Exception as e:
        print(f"Health check failed: {e}")

def test_chat():
    print(f"Starting chat request at {BACKEND_URL}/api/chat ...")
    payload = {"query": "hello"}
    try:
        start = time.time()
        response = requests.post(f"{BACKEND_URL}/api/chat", json=payload, timeout=600)
        duration = time.time() - start
        print(f"Chat status: {response.status_code}")
        print(f"Chat duration: {duration:.2f}s")
    except Exception as e:
        print(f"Chat request failed: {e}")

if __name__ == "__main__":
    # Start a long-running chat request in a separate thread
    chat_thread = threading.Thread(target=test_chat)
    chat_thread.start()
    
    # Wait a moment to ensure chat request has reached backend
    time.sleep(1)
    
    # Run health check while chat is processing
    print("\nAttempting health check while chat is running...")
    test_health()
    
    chat_thread.join()
