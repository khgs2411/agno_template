import os
from dotenv import load_dotenv

load_dotenv()

# Only create server when not in reloader subprocess
if os.environ.get("RUN_MAIN") != "true":
    from app.server import Server
    server = Server()
    app = server.app
else:
    # In reloader subprocess, create a dummy app
    from fastapi import FastAPI
    app = FastAPI()

if __name__ == "__main__":
    # use fastapi dev main.py to run the app with fastapi only
    # use python main.py to run the app with full agent os support
    server.serve()