import os
from pathlib import Path

import pytest
from fastapi.testclient import TestClient


@pytest.fixture(scope="session")
def client(tmp_path_factory):
    # Use isolated SQLite DB per test session
    db_dir = tmp_path_factory.mktemp("db")
    db_path = db_dir / "test.db"
    os.environ["DATABASE_URL"] = f"sqlite:///{db_path}"

    # Import after setting DATABASE_URL so the engine uses the correct path
    from app.main import app  # type: ignore

    with TestClient(app) as c:
        yield c


def test_health(client: TestClient):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_clear_all_initial(client: TestClient):
    r = client.delete("/todos")
    assert r.status_code == 200
    assert isinstance(r.json().get("deleted", 0), int)


def test_create_and_list(client: TestClient):
    # Create
    r = client.post("/todos", json={"title": "Task A"})
    assert r.status_code == 201
    todo_a = r.json()
    assert todo_a["title"] == "Task A"
    assert todo_a["completed"] is False

    r = client.post("/todos", json={"title": "Task B"})
    assert r.status_code == 201

    # List all
    r = client.get("/todos")
    assert r.status_code == 200
    todos = r.json()
    assert len(todos) == 2


def test_update_and_toggle_and_filters(client: TestClient):
    # list to get ids
    r = client.get("/todos")
    assert r.status_code == 200
    todos = r.json()
    assert len(todos) >= 2
    first_id = todos[0]["id"]

    # update title
    r = client.patch(f"/todos/{first_id}", json={"title": "Task A+"})
    assert r.status_code == 200
    assert r.json()["title"] == "Task A+"

    # toggle completion
    r = client.post(f"/todos/{first_id}/toggle")
    assert r.status_code == 200
    assert r.json()["completed"] is True

    # filters
    r = client.get("/todos", params={"status": "completed"})
    assert r.status_code == 200
    completed = r.json()
    assert any(t["id"] == first_id for t in completed)

    r = client.get("/todos", params={"status": "active"})
    assert r.status_code == 200
    active = r.json()
    assert all(t["completed"] is False for t in active)


def test_delete_completed_and_clear_all(client: TestClient):
    # delete completed
    r = client.delete("/todos/completed")
    assert r.status_code == 200
    assert isinstance(r.json().get("deleted", 0), int)

    # clear all
    r = client.delete("/todos")
    assert r.status_code == 200
    assert isinstance(r.json().get("deleted", 0), int)
