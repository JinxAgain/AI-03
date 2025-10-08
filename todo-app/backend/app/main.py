from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
from sqlalchemy.orm import Session

from . import crud, schemas
from .database import Base, engine, get_db
from .models import Todo

app = FastAPI(title="Todo API", version="1.0.0")

# CORS for local development (file:// or http://localhost/static frontends)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten in production
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Create tables on startup
@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/todos", response_model=schemas.TodoOut, status_code=status.HTTP_201_CREATED)
def create_todo(payload: schemas.TodoCreate, db: Session = Depends(get_db)):
    if not payload.title or not payload.title.strip():
        raise HTTPException(status_code=422, detail="Title is required")
    todo = crud.create_todo(db, title=payload.title)
    return todo


@app.get("/todos", response_model=list[schemas.TodoOut])
def list_todos(status: str = "all", db: Session = Depends(get_db)):
    status_normalized = status.lower()
    if status_normalized not in {"all", "active", "completed"}:
        raise HTTPException(status_code=422, detail="Invalid status filter")
    todos = crud.get_todos(db, status=status_normalized)  # type: ignore[arg-type]
    return todos


@app.patch("/todos/{todo_id}", response_model=schemas.TodoOut)
def update_todo(todo_id: int, payload: schemas.TodoUpdate, db: Session = Depends(get_db)):
    todo = crud.get_todo(db, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    updated = crud.update_todo(db, todo, title=payload.title, completed=payload.completed)
    return updated


@app.post("/todos/{todo_id}/toggle", response_model=schemas.TodoOut)
def toggle_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = crud.get_todo(db, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    updated = crud.toggle_todo(db, todo)
    return updated


@app.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = crud.get_todo(db, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    crud.delete_todo(db, todo)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.delete("/todos/completed")
def delete_completed(db: Session = Depends(get_db)):
    count = crud.clear_completed(db)
    return JSONResponse(content={"deleted": count})


@app.delete("/todos")
def delete_all(db: Session = Depends(get_db)):
    count = crud.clear_all(db)
    return JSONResponse(content={"deleted": count})
