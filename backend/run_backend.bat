@echo off
python scripts_init_database.py
python -m uvicorn app.main:app --reload --port 8001
