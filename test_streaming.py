import requests
import json
import time

def test_streaming(query="list all products in table format"):
    url = "http://localhost:8001/api/chat/stream"
    payload = {"query": query}
    
    print(f"Connecting to {url}...")
    start_time = time.time()
    
    try:
        with requests.post(url, json=payload, stream=True) as response:
            if response.status_code == 200:
                print("Connected! Reading stream...")
                
                iterator = response.iter_content(chunk_size=None)
                buffer = b""
                metadata_processed = False
                first_byte_time = None
                
                for chunk in iterator:
                    if not chunk: continue
                    
                    if first_byte_time is None:
                        first_byte_time = time.time()
                        print(f"Time to first byte: {first_byte_time - start_time:.2f}s")
                    
                    if not metadata_processed:
                        buffer += chunk
                        if b"\n" in buffer:
                            parts = buffer.split(b"\n", 1)
                            metadata_line = parts[0]
                            print(f"[METADATA]: {metadata_line.decode('utf-8')}")
                            
                            metadata_processed = True
                            if len(parts) > 1:
                                print(f"[TEXT]: {parts[1].decode('utf-8')}", end="", flush=True)
                    else:
                        print(chunk.decode("utf-8", errors="ignore"), end="", flush=True)
                        
                print("\n\nStream finished.")
                print(f"Total time: {time.time() - start_time:.2f}s")
            else:
                print(f"Error: {response.status_code} - {response.text}")
                
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    test_streaming()
