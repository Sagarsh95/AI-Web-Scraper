
import sys
import os
import asyncio

# 1. Setup path to project root
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)

# 2. Force Proactor Loop for Playwright on Windows
# Must be done before importing uvicorn/fastapi if they init loops
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

import uvicorn
from backend.app.main import app

if __name__ == "__main__":
    print("[INFO] Starting AI Backend (Direct Instance Mode)...")
    try:
        # run(app) keeps it in the same process
        uvicorn.run(app, host="127.0.0.1", port=8001)
    except Exception as e:
        print(f"[FATAL ERROR] Backend crashed: {e}")
        import traceback
        traceback.print_exc()
