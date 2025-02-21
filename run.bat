@echo off
call conda run -n doc-extract-service uvicorn main:app --reload --host 0.0.0.0 --port 8000
pause