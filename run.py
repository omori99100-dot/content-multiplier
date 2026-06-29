import subprocess
import sys
import os
import threading
import time

PRODUCTION = os.getenv("PRODUCTION", "false").lower() == "true"

def run_backend():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    host = "0.0.0.0" if PRODUCTION else "127.0.0.1"
    reload = "" if PRODUCTION else "--reload"
    port = os.getenv("PORT", "8000")
    cmd = [sys.executable, "-m", "uvicorn", "backend.main:app", "--host", host, "--port", port]
    if reload:
        cmd.append(reload)
    subprocess.run(cmd)

def run_frontend():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    port = os.getenv("STREAMLIT_PORT", "8501")
    server_addr = "0.0.0.0" if PRODUCTION else "localhost"
    cmd = [
        sys.executable, "-m", "streamlit", "run", "frontend/app.py",
        "--server.port", port,
        "--server.address", server_addr,
    ]
    if PRODUCTION:
        cmd.extend(["--server.headless", "true"])
    subprocess.run(cmd)

if __name__ == "__main__":
    mode = "PRODUCTION" if PRODUCTION else "DEVELOPMENT"
    print(f"Starting ContentMultiplier AI ({mode})...")
    print(f"Backend: http://localhost:{os.getenv('PORT', '8000')}")
    print(f"Frontend: http://localhost:{os.getenv('STREAMLIT_PORT', '8501')}")
    print(f"API Docs: http://localhost:{os.getenv('PORT', '8000')}/docs")
    if PRODUCTION:
        print("Run frontend and backend separately in production:")
        print("  Backend:  uvicorn backend.main:app --host 0.0.0.0 --port $PORT")
        print("  Frontend: streamlit run frontend/app.py --server.port 8501")
    else:
        t1 = threading.Thread(target=run_backend, daemon=True)
        t2 = threading.Thread(target=run_frontend, daemon=True)
        t1.start()
        time.sleep(2)
        t2.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("Shutting down...")
