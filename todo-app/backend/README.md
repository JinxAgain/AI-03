# Todo Backend (FastAPI + SQLite)

FastAPI backend for the Todo application described in `todo-app/req.md`. Implements CRUD, filters, clear-completed, and clear-all endpoints.

## Requirements
- Python 3.10+
- Windows PowerShell or similar shell

## Setup (Windows)
```powershell
# from directory: todo-app\backend
python -m venv .venv
. .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Run tests
```powershell
# Ensure you run tests from the backend directory so that `app` package is importable
pytest -q
```

## Run server
```powershell
# Development server
uvicorn app.main:app --reload --port 8000
```

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Configuration
- Database file defaults to `sqlite:///./todo.db` under the `backend` directory.
- Override with environment variable:
```powershell
$env:DATABASE_URL = "sqlite:///C:/path/to/your.db"
```

## API Summary
- POST `/todos` — create todo
- GET `/todos?status=all|active|completed` — list todos
- PATCH `/todos/{id}` — partial update (title/completed)
- POST `/todos/{id}/toggle` — toggle completed
- DELETE `/todos/{id}` — delete one
- DELETE `/todos/completed` — clear completed
- DELETE `/todos` — clear all

See `TECH_ARCHITECTURE.md` for full contract.
