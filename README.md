# Telecom Intelligence Assistant

A client-demo prototype for deterministic telecom analytics using a modern React frontend, FastAPI backend, and SQLite as the source of truth.

## Highlights

- **Frontend:** React + Vite + Chart.js
- **Backend:** FastAPI
- **Database:** SQLite (local, file-based)
- **Deterministic analytics flow:** Intent → SQL → Chart → Insight
- **No LLM required**
- **No CSV ingestion tab in UI**
- **Clean telecom branding**

---

## Project Structure

```text
final_tel/
├── backend/
│   ├── app/
│   ├── requirements.txt
│   └── scripts_init_database.py
├── data/
├── database/
├── docs/
└── frontend/
    ├── src/
    └── package.json
```

---

## Prerequisites

- Python 3.10+
- Node.js 18+
- npm 9+

---

## Run Backend

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python scripts_init_database.py
python -m uvicorn app.main:app --reload --port 8001
```

Backend health endpoint:

```text
http://127.0.0.1:8001/health
```

---

## Run Frontend

```powershell
cd frontend
npm install
npm run dev
```

Open:

```text
http://127.0.0.1:5173
```

---

## Environment Configuration

The frontend defaults to backend port `8001`.

If your backend runs on a different port, create `frontend/.env`:

```text
VITE_API_BASE_URL=http://127.0.0.1:8001
```

---

## Demo Queries

Try these in the UI:

- Show churn by region
- Revenue by segment
- Revenue mix by product
- Risk vs revenue scatter
- Monthly churn trend
- Network quality by region

---


