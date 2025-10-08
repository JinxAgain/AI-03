from datetime import datetime
from typing import Iterable, Literal, Optional

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from .models import Todo


def create_todo(db: Session, title: str) -> Todo:
    todo = Todo(title=title.strip(), completed=False)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


def get_todos(db: Session, status: Literal["all", "active", "completed"] = "all") -> Iterable[Todo]:
    stmt = select(Todo)
    if status == "active":
        stmt = stmt.where(Todo.completed.is_(False))
    elif status == "completed":
        stmt = stmt.where(Todo.completed.is_(True))
    return db.execute(stmt.order_by(Todo.id.desc())).scalars().all()


def get_todo(db: Session, todo_id: int) -> Optional[Todo]:
    return db.get(Todo, todo_id)


def update_todo(db: Session, todo: Todo, *, title: Optional[str] = None, completed: Optional[bool] = None) -> Todo:
    if title is not None:
        todo.title = title.strip()
    if completed is not None:
        todo.completed = bool(completed)
    # ensure updated_at changes
    todo.updated_at = datetime.utcnow()
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


def toggle_todo(db: Session, todo: Todo) -> Todo:
    todo.completed = not bool(todo.completed)
    todo.updated_at = datetime.utcnow()
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


def delete_todo(db: Session, todo: Todo) -> None:
    db.delete(todo)
    db.commit()


def clear_completed(db: Session) -> int:
    stmt = delete(Todo).where(Todo.completed.is_(True))
    result = db.execute(stmt)
    db.commit()
    # SQLite returns rowcount reliably for DELETE
    return result.rowcount or 0


def clear_all(db: Session) -> int:
    stmt = delete(Todo)
    result = db.execute(stmt)
    db.commit()
    return result.rowcount or 0
