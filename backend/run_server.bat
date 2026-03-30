@echo off
cd /d E:\FYP\backend
call venv\Scripts\activate.bat
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
