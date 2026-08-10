from datetime import date, timedelta

from fastapi.testclient import TestClient


def test_create_task_valid_returns_201_with_full_body(client: TestClient):
    response = client.post(
        "/tasks",
        json={
            "title": "Create task test",
            "description": "Task description",
            "status": "ToDo",
            "priority": "High",
            "assignee": "Ada",
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert set(body) == {
        "id",
        "title",
        "description",
        "status",
        "priority",
        "assignee",
        "due_date",
        "created_at",
        "updated_at",
        "is_overdue",
    }
    assert body["title"] == "Create task test"
    assert body["description"] == "Task description"
    assert body["status"] == "ToDo"
    assert body["priority"] == "High"
    assert body["assignee"] == "Ada"
    assert body["due_date"] is None
    assert body["is_overdue"] is False
    assert body["id"]
    assert body["created_at"]
    assert body["updated_at"]


def test_create_task_missing_title_returns_422(client: TestClient):
    response = client.post("/tasks", json={})

    assert response.status_code == 422


def test_create_task_blank_title_returns_422(client: TestClient):
    response = client.post("/tasks", json={"title": "   "})

    assert response.status_code == 422


def test_create_task_invalid_priority_returns_422(client: TestClient):
    response = client.post("/tasks", json={"title": "Invalid priority", "priority": "Urgent"})

    assert response.status_code == 422


def test_create_task_unknown_field_returns_422(client: TestClient):
    response = client.post("/tasks", json={"title": "Unknown field", "unexpected": True})

    assert response.status_code == 422


def test_create_task_valid_due_date_returns_due_date_and_overdue_state(client: TestClient):
    due_date = date.today() + timedelta(days=2)

    response = client.post(
        "/tasks",
        json={"title": "Scheduled task", "due_date": due_date.isoformat()},
    )

    assert response.status_code == 201
    assert response.json()["due_date"] == due_date.isoformat()
    assert response.json()["is_overdue"] is False


def test_create_task_invalid_due_date_returns_422(client: TestClient):
    response = client.post(
        "/tasks",
        json={"title": "Invalid date", "due_date": "August 3"},
    )

    assert response.status_code == 422


def test_list_tasks_empty_returns_200_and_empty_list(client: TestClient):
    response = client.get("/tasks")

    assert response.status_code == 200
    assert response.json() == []


def test_list_tasks_filter_by_status_no_match_returns_200_and_empty_list(client: TestClient):
    client.post("/tasks", json={"title": "To do task"})

    response = client.get("/tasks", params={"status": "Done"})

    assert response.status_code == 200
    assert response.json() == []


def test_list_tasks_filter_by_priority_returns_only_matches(client: TestClient):
    client.post("/tasks", json={"title": "Low task", "priority": "Low"})
    client.post("/tasks", json={"title": "High task", "priority": "High"})

    response = client.get("/tasks", params={"priority": "High"})

    assert response.status_code == 200
    assert [task["title"] for task in response.json()] == ["High task"]


def test_list_tasks_overdue_filter_returns_only_overdue_tasks(client: TestClient):
    past_date = (date.today() - timedelta(days=1)).isoformat()
    today = date.today().isoformat()
    client.post("/tasks", json={"title": "Overdue high", "due_date": past_date, "priority": "High"})
    client.post("/tasks", json={"title": "Due today", "due_date": today, "priority": "High"})
    client.post(
        "/tasks",
        json={"title": "Completed task", "due_date": past_date, "status": "Done", "priority": "High"},
    )

    response = client.get("/tasks", params={"overdue": "true", "priority": "High"})

    assert response.status_code == 200
    assert [task["title"] for task in response.json()] == ["Overdue high"]
    assert response.json()[0]["is_overdue"] is True


def test_get_task_by_id_returns_task(client: TestClient, created_task: dict):
    response = client.get(f"/tasks/{created_task['id']}")

    assert response.status_code == 200
    assert response.json() == created_task


def test_get_task_by_id_not_found_returns_404_with_detail(client: TestClient):
    task_id = "missing-task-id"

    response = client.get(f"/tasks/{task_id}")

    assert response.status_code == 404
    assert response.json() == {"detail": f"Task with id {task_id} not found"}


def test_patch_partial_update_keeps_other_fields(client: TestClient, created_task: dict):
    response = client.patch(
        f"/tasks/{created_task['id']}",
        json={"priority": "High"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["title"] == "fixture task"
    assert body["description"] == ""
    assert body["status"] == "ToDo"
    assert body["priority"] == "High"
    assert body["assignee"] is None
    assert body["due_date"] is None
    assert body["created_at"] == created_task["created_at"]


def test_patch_due_date_can_be_changed_and_cleared(client: TestClient, created_task: dict):
    due_date = (date.today() + timedelta(days=5)).isoformat()

    updated_response = client.patch(
        f"/tasks/{created_task['id']}",
        json={"due_date": due_date},
    )
    cleared_response = client.patch(
        f"/tasks/{created_task['id']}",
        json={"due_date": None},
    )

    assert updated_response.status_code == 200
    assert updated_response.json()["due_date"] == due_date
    assert cleared_response.status_code == 200
    assert cleared_response.json()["due_date"] is None


def test_patch_not_found_returns_404(client: TestClient):
    task_id = "missing-task-id"

    response = client.patch(f"/tasks/{task_id}", json={"title": "Updated title"})

    assert response.status_code == 404
    assert response.json() == {"detail": f"Task with id {task_id} not found"}


def test_patch_valid_transition_todo_to_inprogress_returns_200(
    client: TestClient,
    created_task: dict,
):
    response = client.patch(
        f"/tasks/{created_task['id']}",
        json={"status": "InProgress"},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "InProgress"


def test_patch_invalid_transition_todo_to_done_returns_422(
    client: TestClient,
    created_task: dict,
):
    response = client.patch(
        f"/tasks/{created_task['id']}",
        json={"status": "Done"},
    )

    assert response.status_code == 422
    assert "Invalid status transition from ToDo to Done" in response.json()["detail"]


def test_patch_same_status_returns_422(client: TestClient, created_task: dict):
    response = client.patch(
        f"/tasks/{created_task['id']}",
        json={"status": "ToDo"},
    )

    assert response.status_code == 422
    assert "Invalid status transition from ToDo to ToDo" in response.json()["detail"]


def test_delete_existing_returns_204_no_body(client: TestClient, created_task: dict):
    response = client.delete(f"/tasks/{created_task['id']}")

    assert response.status_code == 204
    assert response.content == b""


def test_delete_missing_returns_404(client: TestClient):
    task_id = "missing-task-id"

    response = client.delete(f"/tasks/{task_id}")

    assert response.status_code == 404
    assert response.json() == {"detail": f"Task with id {task_id} not found"}


def test_create_task_generates_created_activity_event(client: TestClient):
    created_task = client.post("/tasks", json={"title": "Activity task"}).json()

    response = client.get("/activity")

    assert response.status_code == 200
    assert response.json()[0]["event_type"] == "created"
    assert response.json()[0]["task_id"] == created_task["id"]
    assert response.json()[0]["details"] == {"title": "Activity task"}


def test_patch_non_status_update_generates_updated_activity_event(
    client: TestClient,
    created_task: dict,
):
    client.patch(f"/tasks/{created_task['id']}", json={"priority": "High"})

    response = client.get("/activity")

    assert response.status_code == 200
    assert response.json()[0]["event_type"] == "updated"
    assert response.json()[0]["details"] == {"changed_fields": ["priority"]}


def test_patch_status_change_generates_from_and_to_activity_event(
    client: TestClient,
    created_task: dict,
):
    client.patch(f"/tasks/{created_task['id']}", json={"status": "InProgress"})

    response = client.get("/activity")

    assert response.status_code == 200
    assert response.json()[0]["event_type"] == "status_changed"
    assert response.json()[0]["details"] == {
        "from_status": "ToDo",
        "to_status": "InProgress",
    }


def test_delete_permanently_removes_task_and_generates_activity_event(
    client: TestClient,
    created_task: dict,
):
    delete_response = client.delete(f"/tasks/{created_task['id']}")
    active_response = client.get("/tasks")
    get_response = client.get(f"/tasks/{created_task['id']}")
    activity_response = client.get("/activity")

    assert delete_response.status_code == 204
    assert active_response.json() == []
    assert get_response.status_code == 404
    assert activity_response.json()[0]["event_type"] == "deleted"
    assert activity_response.json()[0]["task_id"] == created_task["id"]
    assert activity_response.json()[0]["details"] == {"title": "fixture task"}
