import pytest
from fastapi.testclient import TestClient

from app import storage
from app.main import app


@pytest.fixture(autouse=True)
def _reset_storage(tmp_path):
    previous_paths = storage._configure_storage(
        tmp_path / "tasks.json",
        tmp_path / "activity.json",
    )
    storage._reset()
    yield
    storage._reset()
    storage._restore_storage(previous_paths)


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def created_task(client: TestClient) -> dict:
    response = client.post("/tasks", json={"title": "fixture task"})
    assert response.status_code == 201
    return response.json()
