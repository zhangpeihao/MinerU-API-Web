import subprocess
import sys
import os
import argparse

def run_server(env_name="doc-extract-service", port=8000):
    command = [
        "conda", "run",
        "-n", env_name,
        "uvicorn", "main:app",
        "--reload",
        "--host", "0.0.0.0",
        "--port", str(port)
    ]
    
    try:
        subprocess.run(command)
    except KeyboardInterrupt:
        print("\nServer stopped")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run FastAPI server with conda")
    parser.add_argument(
        "--env",
        default="doc-extract-service",
        help="Conda environment name"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port to run the server on"
    )
    
    args = parser.parse_args()
    run_server(args.env, args.port)